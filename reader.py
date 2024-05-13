import collections, copy, csv
import collections.abc
from abc import ABC, abstractmethod


class DataCollection(collections.abc.Sequence):
    def __init__(self, headers, types):
        self.col_count = len(headers)
        self.headers = headers
        self.types = types
        self.data = [[] for _ in range(len(headers))]

    def __len__(self):
        return len(self.data[0]) if self.col_count > 0 else 0

    def __getitem__(self, value):
        if isinstance(value, slice):
            data = DataCollection(copy.deepcopy(self.headers), copy.deepcopy(self.types))
            data.data = [col[value] for col in self.data]
            return data

        return dict(zip(self.headers, (col[value] for col in self.data)))

    def append(self, list):
        for index in range(self.col_count):
            self.data[index].append(self.types[index](list[index]))


def read_csv_as_dicts_old(filename, types):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)

        if len(headers) != len(types):
            print("Error: Length of types does not match data count")
            return []
        
        return [{ name:typed(value) for name, typed, value in zip(headers, types, row) } for row in rows]


def read_csv_as_columns(filename, types):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)

        if len(headers) != len(types):
            print("Error: Length of types does not match data count")
            return DataCollection([], [])
        
        data = DataCollection(headers, types)
        for row in rows:
            data.append(row)
        return data


def read_csv_as_instances_old(filename, cls):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records



def read_csv_as_instances(filename, cls):
    return InstanceCSVParser(cls).parse(filename)

def read_csv_as_dicts(filename, types):
    return DictCSVParser(types).parse(filename)


class CSVParser(ABC):

    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass

class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }

class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)
    

if __name__ == '__main__':
    from sys import intern
    import tracemalloc
    tracemalloc.start()
    rows = read_csv_as_columns('Data/ctabus.csv', [intern, intern, str, int])
    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())

# Current 96724503, Peak 96754552 (csv as columns)
# Current 35330133, Peak 35360292 (csv as columns, with intern route/dates)
