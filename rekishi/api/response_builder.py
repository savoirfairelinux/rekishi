from django.http import HttpResponse, Http404
from functools import wraps
import json

def dygraph_response(view_funct):
    @wraps(view_funct)
    def wrapper(*args, **kwargs):
        data = view_funct(*args, **kwargs)
        ret_value = json.dumps([series.to_dygraph() for series in data], 
                indent=2)
        return HttpResponse(ret_value, content_type='application/json')

    return wrapper
