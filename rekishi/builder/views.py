from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import db
from . import influxdb_dataset, influxdb_series
from forms import QueryForm

import json

def index(request):
    if request.method == 'GET':
        form = QueryForm()
        return render(request, 'builder/index.html', {
            'form': form,
        })
        # Render Form
    elif request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            
            query = 'SELECT %s FROM %s.%s.%s;' % (
                    form.cleaned_data['field'],
                    form.cleaned_data['host'], 
                    form.cleaned_data['service'], 
                    form.cleaned_data['series']
                )
            data = db.query(query)
            data = influxdb_dataset(data)
            ret_value = json.dumps([series.to_dygraph() for series in data], indent=2)

            return render(request, 'api/basicgraph.html', {
                'data': ret_value,
                'query': query
            })
        # Return Redirect to graph

def bypass(request):
    query = request.GET.get('q', '')

    data = db.query(query)
    data = influxdb_dataset(data)
    ret_value = json.dumps([series.to_dygraph() for series in data], indent=2)

    # response = HttpResponse(ret_value)
    # response['Content-Type'] = "application/json"

    return render(request, 'basicgraph.html', {
        'data': ret_value,
        'query': query
    })
