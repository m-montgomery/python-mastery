import csv
import collections
import collections.abc


# sorted results:
# Current  96725614, Peak  96754311 (list columns / RideData)
# Current 128449630, Peak 128479607 (tuples)
# Current 138970937, Peak 139000806 (class instances with slots)
# Current 148212585, Peak 148242510 (named tuples)
# Current 194416985, Peak 194446854 (class instances)
# Current 220859318, Peak 220889295 (dictionaries)


# Current 128449630, Peak 128479607
def read_rides_as_tuples(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records


RowTuple = collections.namedtuple('RowTuple', ['route', 'date', 'daytype', 'rides'])


# Current 148212585, Peak 148242510
def read_rides_as_named_tuples(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)     # Skip headers
        for row in rows:
            records.append(RowTuple(*row))
    return records


# Current 220859318, Peak 220889295
def read_rides_as_dictionaries(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)     # Skip headers
        for row in rows:
            records.append({
                'route': row[0],
                'date': row[1],
                'daytype': row[2],
                'rides': int(row[3]),
            })
    return records


class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


# Current 194416985, Peak 194446854
def read_rides_as_class_instances(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)     # Skip headers
        for row in rows:
            records.append(Row(*row))
    return records


class RowSlots:
    __slots__ = ('route', 'date', 'daytype', 'rides')

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


# Current 138970937, Peak 139000806
def read_rides_as_class_instances_with_slots(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)     # Skip headers
        for row in rows:
            records.append(RowSlots(*row))
    return records


# Current 96725614, Peak 96754311
def read_rides_as_columns(filename):
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)     # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


class RideData(collections.abc.Sequence):
    def __init__(self, routes = [], dates = [], daytypes = [], numrides = []):
        # Each value is a list with all of the values (a column)
        self.routes = routes
        self.dates = dates
        self.daytypes = daytypes
        self.numrides = numrides

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, value):
        if isinstance(value, slice):
            return RideData(
                routes=self.routes[value],
                dates=self.dates[value],
                daytypes=self.daytypes[value],
                numrides=self.numrides[value],
            )
        return { 'route': self.routes[value],
                 'date': self.dates[value],
                 'daytype': self.daytypes[value],
                 'rides': self.numrides[value] }

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])


# Current 96724414, Peak 96754463
def read_rides_as_ride_data(filename):
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)     # Skip headers
        for row in rows:
            records.append({
                'route': row[0],
                'date': row[1],
                'daytype': row[2],
                'rides': int(row[3]),
            })
    return records


if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    rows = read_rides_as_ride_data('Data/ctabus.csv')
    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
