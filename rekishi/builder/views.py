
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rekishi.api.response_builder import jsonify_series

from rekishi.builder.forms import QueryForm

from rekishi.utils.influx import query_influx_2


def index(request):

    if request.method == 'POST':
        args = (request.POST,)
    else:
        args = ()

    form = QueryForm(*args)

    if form.is_valid():
        print form.cleaned_data

        query = 'SELECT %s FROM %s.%s.%s;' % (
                form.cleaned_data['field'],
                form.cleaned_data['host'],
                form.cleaned_data['service'],
                form.cleaned_data['series']
            )


        json_data = jsonify_series(query_influx_2(query, {}))

        return render(request, 'api/basicgraph.html', {
            'data': json_data,
            'query': query
        })

    return render(request, 'builder/index.html', { 'form': form })


def bypass(request):
    query = request.GET.get('q', '')

    json_data = jsonify_series(query_influx_2(query, {}))

    return render(request, 'basicgraph.html', {
        'data': json_data,
        'query': query
    })
