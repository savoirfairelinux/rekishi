
from collections import OrderedDict

from rekishi.utils.influx import query_influx


def index(request, host=None, service=None, serie=None, supplementary_kw=None):

    # request.GET is a special dict, which can have multiple values per key.
    # using its .items() method ensure the get only the last value
    query_kw = dict(request.GET.items())

    if supplementary_kw:
        query_kw.update(supplementary_kw)

    base_kw = OrderedDict()
    if host is None:
        host = '.*'
    base_kw['host'] = host

    if service is None:
        service = '.*'
    base_kw['service'] = service

    return query_influx(base_kw, query_kw, get_events=True)
