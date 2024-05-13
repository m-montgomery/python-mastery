# reader.py

import csv

from typing import List, Dict, TypeVar, Iterable

T = TypeVar('T')

def read_csv_as_dicts(filename:str, types:List, headers:List[str]=None) -> List[Dict[str, any]]:
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    with open(filename) as file:
        return csv_as_dicts(file, types, headers)

def read_csv_as_instances(filename:str, cls:T, headers:List[str]=None) -> List[T]:
    '''
    Read CSV data into a list of instances
    '''
    with open(filename) as file:
        return csv_as_instances(file, cls, headers)

def csv_as_dicts(lines:Iterable[str], types:List[type], headers:List[str]) -> List[Dict[str, any]]:
    '''
    Read CSV-formatted lines into a list of dictionaries with type conversion
    '''
    # records = []
    # rows = csv.reader(lines)
    # if not headers:
    #     headers = next(rows)
    # for row in rows:
    #     record = { name: func(val) 
    #                 for name, func, val in zip(headers, types, row) }
    #     records.append(record)
    # return records

    return convert_csv(lines, lambda headers,row: { name: func(val) for name, func, val in zip(headers, types, row) }, headers=headers)

def csv_as_instances(lines:Iterable[str], cls:T, headers:List[str]) -> List[T]:
    '''
    Read CSV-formatted lines into a list of instances
    '''
    # records = []
    # rows = csv.reader(lines)
    # if not headers:
    #     headers = next(rows)
    # for row in rows:
    #     record = cls.from_row(row)
    #     records.append(record)
    # return records
    
    return convert_csv(lines, lambda h,row: cls.from_row(row), headers=headers)

def parse_line(line):
    try:
        entries = line.strip().split('=')
        return (entries[0], entries[1]) if len(entries) == 2 else None
    except:
        return None


def convert_csv(lines:Iterable[str], convert, *, headers:List[str] = None) -> List[T]:
    '''
    Read CSV-formatted lines and convert with user-defined function
    '''
    rows = csv.reader(lines)
    if not headers:
        headers = next(rows)

    return list(map(lambda row: convert(headers, row), rows))
