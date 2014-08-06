import datetime

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
            new_point = []
            point.pop(seq_num_idx)

        return series

    def _convert_timestamps(self, series):
        timestamp_idx = series['labels'].index('time')
        for point in series['data']:
            point[timestamp_idx] = datetime.datetime.fromtimestamp(
                int(point[timestamp_idx])
            ).strftime('%Y/%m/%d %H:%M:%S')
        
        return series
