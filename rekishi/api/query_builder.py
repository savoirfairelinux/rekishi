

class InfluxQueryHelper(object):

    def __init__(self):
        self.where_clause = ''
        self.limit_clause = ''
        self.query = ''

    def build_query(self, base_query, **kwargs):

        where_clause_dict = {}
        if 'start' in kwargs:
            start = kwargs['start']
            if isinstance(start, (int, float)):
                start = '%ss' % int(start)
            where_clause_dict['start'] = start
        if 'end' in kwargs:
            end = kwargs['end']
            if isinstance(end, (int, float)):
                end = '%ss' % int(end)
            where_clause_dict['end'] = end
        if 'where' in kwargs:
            where_clause_dict['where'] = kwargs['where']
        if len(where_clause_dict) > 0:
            self.where_clause = self.build_where_clause(where_clause_dict)

        if 'limit' in kwargs:
            self.limit_clause = self.build_limit_clause(kwargs['limit'])

        # SELECT * FROM SERIE_NAME WHERE TIME=XX LIMIT 1;
        self.query = "%s%s%s;" % (base_query, self.where_clause, self.limit_clause)
        return self.query

    def build_limit_clause(self, limit):
        return ' limit %s' % (limit)

    def build_where_clause(self, where_dict):

        where_clause = ''
        for key, value in where_dict.iteritems():
            new_segment = ''
            # Where clause still empty
            if where_clause == '':
                new_segment += ' WHERE '
            else:
                new_segment += ' AND '

            if key == 'start':
                new_segment += 'time > %s' % value
                where_clause += new_segment

            elif key == 'end':
                new_segment += 'time < %s' % value
                where_clause += new_segment

            # Where list
            elif key == 'where':
                cond_list = value.split(';')
                for cond in cond_list:
                    if where_clause == '':
                        new_segment = ' WHERE '
                    else:
                        new_segment = ' AND '

                    try:
                        wkey, wop, wval = cond.split(',')
                        new_segment += '%s %s %s' % (wkey, wop, wval)
                        where_clause += new_segment
                    except:
                        new_segment = ''
                        raise ValueError('Invalid WHERE clause.')

        return where_clause
