from django.shortcuts import render
from django.http import HttpResponse, Http404
from . import db
from . import influxdb_dataset, influxdb_series

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

def simple_series(request, host=None, service=None, series=None):
    
    series = '.'.join([host, service, series])
    query = 'SELECT * FROM %s;' % series

    data = db.query(query)
    data = influxdb_dataset(data)
    ret_value = json.dumps([series.to_dygraph() for series in data], indent=2)

    return HttpResponse(ret_value, content_type="application/json")
    # return render(request, 'api/basicgraph.html', {
    #     'data': ret_value,
    #     'query': query
    # })

def host_series(request, host=None):

    try:
        query = 'SELECT * from /%s\.%s.*/;' % (host, "_self_")

        data = db.query(query)
        print query
        print data
        data = influxdb_dataset(data)
        ret_value = json.dumps([series.to_dygraph() for series in data], indent=2)

        return HttpResponse(ret_value, content_type="application/json")

    except:
        raise Http404

    return HttpResponse(ret_value, content_type="application/json")

def service_series(request, host=None, service=None):

    try:
        query = 'SELECT * from /%s\.%s.*/;' % (host, service)

        data = db.query(query)
        data = influxdb_dataset(data)
        print json.dumps(data, indent=2)
        ret_value = json.dumps([series.to_dygraph() for series in data], indent=2)

        return HttpResponse(ret_value, content_type="application/json")

    except:
        raise Http404

    return HttpResponse(ret_value, content_type="application/json")
