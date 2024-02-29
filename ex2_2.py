import readrides
from collections import Counter

"""
1. How many bus routes exist in Chicago?
2. How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing?
3. What is the total number of rides taken on each bus route?
4. What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?
"""


def get_bus_routes(rows):
    routes = {row.route for row in rows}
    return routes


def calculate_riders(rows, route, date):
    sorted_rows = {(row.route, row.date): int(row.rides) for row in rows}
    return sorted_rows.get((route, date), 0)


def calculate_total_rides_per_route(rows):
    totals = Counter()
    for row in rows:
        totals[row.route] += int(row.rides)
    return totals


def calculate_total_rides_per_route_per_year(rows):
    totals = Counter()
    for row in rows:
        totals[(row.route, row.date[6:])] += int(row.rides)
    return totals


def calculate_top_route_increases(rows, num=5):
    rides_per_year = calculate_total_rides_per_route_per_year(rows)
    routes = get_bus_routes(rows)

    increases = Counter({route: rides_per_year[(route, '2011')] - rides_per_year[(route, '2001')] for route in routes})
    return increases.most_common(num)


if __name__ == '__main__':
    rows = readrides.read_rides_as_named_tuples('Data/ctabus.csv')

    print(f"\nQ1: {len(get_bus_routes(rows))}")

    print(f"\nQ2: {calculate_riders(rows, '22', '02/02/2011')}")

    totals = calculate_total_rides_per_route(rows)
    print("\nQ3:")
    for route in sorted(totals.keys()):
        print(f"{route}: {totals[route]}")

    print(f"\nQ4: {calculate_top_route_increases(rows)}")
