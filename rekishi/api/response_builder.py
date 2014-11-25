
import json
from functools import wraps


from django.http import HttpResponse, Http404
from rekishi.utils.influx import InfluxDbSerie


def jsonify_series(series):
    return json.dumps(
        [
            InfluxDbSerie(serie).to_dygraph()
            for serie in series
        ],
         indent=2
    )


def dygraph_response(series):
    return HttpResponse(jsonify_series(series), content_type='application/json')


def dygraph_response_wrapper(view_funct):
    @wraps(view_funct)
    def wrapper(*args, **kwargs):
        series = view_funct(*args, **kwargs)
        return dygraph_response(series)
    return wrapper
