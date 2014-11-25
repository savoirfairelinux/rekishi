

from functools import wraps
import operator


def filter_data_events():
    def wrapper(func):
        @wraps(func)
        def wrapped(request, *a, **kw):
            data = func(request, *a, **kw)
            # Handle the removal of events series if not queried for
            op = lambda d: operator.contains(d, '._events_.')
            if request.GET.get('events', '').lower() == 'true':
                op = lambda d: not op(d)
            return filter(lambda d: op(d.get('name', '')), data)
        return wrapped
    return wrapper