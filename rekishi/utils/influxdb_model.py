class influxdb_dataset(list):
    def __init__(self, *args):
        super(influxdb_dataset, self).__init__(*args)
        for i,x in enumerate(self):
            super(influxdb_dataset, self).__setitem__(i, influxdb_series(x))

class influxdb_series(dict):
    def to_dygraph(self):
        series = {}
        series['labels'] = self.get('columns')
        series['data'] = self.get('points')
        return series

    def to_csv(self):
        pass

