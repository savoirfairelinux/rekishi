from django.shortcuts import render
from django.http import HttpResponse, Http404
from . import db
from . import influxdb_dataset, influxdb_series
from response_builder import dygraph_response
from query_builder import InfluxQueryHelper

import json

def index(request):
    return HttpResponse("Check /api/bypass?q=QUERYHERE")

def bypass(request):
    query = request.GET.get('q', '')

    data = db.query(query)
    data = influxdb_dataset(data)
    ret_value = json.dumps([series.to_dygraph() for series in data], indent=2)

    # response = HttpResponse(ret_value)
    # response['Content-Type'] = "application/json"

    return render(request, 'api/basicgraph.html', {
        'data': ret_value,
        'query': query
    })

@dygraph_response
def dg_single_series(request, host=None, service=None, series=None):
    
    try: 
        host = host.replace('.', '_')
        service = service.replace('.', '_')
        series = series.replace('.', '_')
        series = '.'.join([host, service, series])
        base = 'SELECT * FROM %s' % series

        query_helper = InfluxQueryHelper()
        query = query_helper.build_query(base, **request.GET)

        data = db.query(query)
        data = influxdb_dataset(data)

        # Handle the removal of events series if not queried for
        if request.GET.get('events', 'false').lower() != 'true':
            data = [series for series in data if series.get('name',
                    '').find('._events_.') < 0]

        return data

    except Exception as e:
        print e
        raise Http404

@dygraph_response
def dg_host_series(request, host=None):

    try:
        
        host = host.replace('.', '_')
        base = "SELECT * FROM /%s\.%s\..*/" % (host, "_self_")
        base = "SELECT * FROM /%s\..*/" % host

        query_helper = InfluxQueryHelper()
        query = query_helper.build_query(base, **request.GET)

        data = db.query(query)
        data = influxdb_dataset(data)

        # Handle the removal of events series if not queried for
        if request.GET.get('events', 'false').lower() != 'true':
            data = [series for series in data if series.get('name',
                    '').find('._events_.') < 0]

        return data

    except Exception as e:
        print e
        raise Http404

@dygraph_response
def dg_service_series(request, host=None, service=None):

    try:
        host = host.replace('.', '_')
        service = service.replace('.', '_')
        base = 'SELECT * FROM /%s\.%s\.%s\..*/' % (host, service, "_self_")

        query_helper = InfluxQueryHelper()
        query = query_helper.build_query(base, **request.GET)

        data = db.query(query)
        data = influxdb_dataset(data)

        # Handle the removal of events series if not queried for
        if request.GET.get('events', 'false').lower() != 'true':
            data = [series for series in data if series.get('name',
                    '').find('._events_.') < 0]

        return data

    except Exception as e:
        print e
        raise Http404
