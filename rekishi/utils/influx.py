
from __future__ import absolute_import


import datetime
import logging

logger = logging.getLogger('influxdb')

import django.conf

import influxdb

from rekishi.api.query_builder import InfluxQueryHelper


#############################################################################
#
# copied/duplicated from (so to not depends on) : mod-influxdb
#
_serie_separator = '>'

def _escape_serie_name_value(value):
    ''' escape the '>' char (with usual '\') as it's used as item separator in the serie name.
     and so also escape the '\' as it's used as escape char.
     '\' have to be escaped first..
    '''
    return value.replace('\\', r'\\').replace(_serie_separator, r'\%s' % _serie_separator)

def encode_serie_name(*args, **kw):
    front = kw.pop('front', None)
    if kw:
        raise TypeError('Unexpected keyword argument to encode_serie_name: %s' % repr(kw))
    ret = _serie_separator.join(_escape_serie_name_value(arg) for arg in args)
    if front is not None:
        ret = '%s%s%s' % (front, _serie_separator, ret)
    return ret

def decode_serie_name(serie_name):
    idx = 0
    ret = []
    cur = []
    while idx < len(serie_name):
        char = serie_name[idx]
        if char == '\\':
            idx += 1
            if idx >= len(serie_name):
                logger.warning('Invalid encoded serie name: escape char (\) on end of name without additional char ; serie_name=%r' % serie_name)
                char = ''
            else:
                char = serie_name[idx]
            cur.append(char)
        elif char == _serie_separator:
            ret.append(''.join(cur))
            cur = []
        else:
            cur.append(char)
        idx += 1
    if cur:
        ret.append(''.join(cur))
    return ret

#############################################################################


class InfluxDbSerie(dict):

    def to_dygraph(self):
        series = {}
        series['name'] = self.get('name')
        series['labels'] = self.get('columns')
        series['data'] = self.get('points')
        series['data'].reverse()

        if "sequence_number" in series['labels']:
            series = self._strip_sequence_numbers(series)
        # series = self._convert_timestamps(series)
        return series

    def to_csv(self):
        pass

    def _strip_sequence_numbers(self, series):
        seq_num_idx = series['labels'].index('sequence_number')
        series['labels'].remove('sequence_number')
        for point in series['data']:
            point.pop(seq_num_idx)

        return series


    def _convert_timestamps(self, series):
        timestamp_idx = series['labels'].index('time')
        for point in series['data']:
            point[timestamp_idx] = datetime.datetime.fromtimestamp(
                int(point[timestamp_idx])
            ).strftime('%Y/%m/%d %H:%M:%S')
        
        return series


def query_influx_2(query, query_kw):

    query_helper = InfluxQueryHelper()
    query = query_helper.build_query(query, **query_kw)

    db = make_influxdb_conn()
    series = db.query(query)

    return series


def query_influx(base_kw, query_kw, what='*', get_events=False):
    ''' Execute an influx db query.
    :param base_kw: The "base" arguments of the query. Must comes in an OrderedDict.
        Actually only the values are used.
    :type base_kw: collections.OrderedDict
    :type query_kw: django.http.request.QueryDict or simply a dict.
    :type what: str
    :return: The data from influxdb matching the given arguments.
    '''

    if isinstance(query_kw,  django.http.request.QueryDict):
        query_kw = dict(query_kw.items())

    base = encode_serie_name(*base_kw.values())

    if get_events:
        base = encode_serie_name('_events_', '.*', front=base)

     # if there are some '\' in the base we must escape them !
        # remember the FROM is a regex here..
    query = "SELECT %s FROM /^%s$/" % (what, base.replace('\\', r'\\'))
    # or more simply (as we do exact search) :
    # but we still have to escape double quote ofcourse..
    #query = 'SELECT %s FROM "%s"' % (what, base.replace('"', r'\"'))

    return query_influx_2(query, query_kw)


def make_influxdb_conn(settings=None):
    settings = settings or django.conf.settings

    return influxdb.InfluxDBClient(
        settings.INFLUXDB_HOST, settings.INFLUXDB_PORT,
        settings.INFLUXDB_USER, settings.INFLUXDB_PASSWORD,
        settings.INFLUXDB_DB
    )