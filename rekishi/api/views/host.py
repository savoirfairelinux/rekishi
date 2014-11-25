

from __future__ import absolute_import


import json
from urllib import unquote
from collections import OrderedDict


from django.shortcuts import render
from rekishi.api.response_builder import jsonify_series

from rekishi.utils.influx import query_influx, query_influx_2


def bypass(request):
    query = request.GET.get('q', '')

    json_data = jsonify_series(query_influx_2(query, {}))

    return render(request, 'api/basicgraph.html', {
        'data': json_data,
        'query': query
    })


def dg_host_series(request, host):

    base_kw = OrderedDict()
    base_kw['host'] = host
    base_kw['service'] = '_self_'
    base_kw['serie'] = '.*'

    get_events = request.GET.get('events', '').lower() == 'true'

    return query_influx(base_kw, request.GET, get_events=get_events)


def dg_service_series(request, host, service):

    base_kw = OrderedDict()
    base_kw['host'] = host
    base_kw['service'] = service
    base_kw['serie'] = '.*'

    get_events = request.GET.get('events', '').lower() == 'true'

    return query_influx(base_kw, request.GET, get_events=get_events)


def dg_single_series(request, host, service, serie):

    base_kw = OrderedDict()
    base_kw['host'] = host
    base_kw['service'] = service
    base_kw['serie'] = unquote(serie)

    get_events = request.GET.get('events', '').lower() == 'true'

    return query_influx(base_kw, request.GET, get_events=get_events)
