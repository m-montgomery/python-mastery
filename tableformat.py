from abc import ABC, abstractmethod

class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        pass

    @abstractmethod
    def row(self, rowdata):
        pass

class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))
    
    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))

class CSVFormatter(TableFormatter):
    def headings(self, headers):
        print(','.join(headers))

    def row(self, rowdata):
        print(','.join(str(d) for d in rowdata))

class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print(f"<tr> {' '.join('<th>' + header + '</th>' for header in headers)} </tr>")

    def row(self, rowdata):
        print(f"<tr> {' '.join('<td>' + str(data) + '</td>' for data in rowdata)} </tr>")

def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError('Expected a TableFormatter')
    formatter.headings(fields)
    for record in records:
        rowdata = [getattr(record, field) for field in fields]
        formatter.row(rowdata)

def create_formatter(format, upper_headers=False, column_formats=[]):
    formatters = {
        'text': TextTableFormatter,
        'csv': CSVFormatter,
        'html': HTMLTableFormatter
    }
    if format not in formatters:
        raise ValueError('Unknown format %s' % format)

    main_formatter = formatters[format]()
    
    if not upper_headers and not column_formats:
        return main_formatter
    
    parent_classes = [formatters[format]]
    if upper_headers:
        parent_classes.insert(0, UpperHeadersMixin)
    if column_formats:
        parent_classes.insert(0, ColumnFormatMixin)

    class SpecialFormatter(*parent_classes):
        formats = column_formats
    return SpecialFormatter()


class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])



def print_table_orig(data, fields):
    for field in fields:
        print('%10s ' % (field), end="")
    print()
    print("---------- " * len(fields))
    for entry in data:
        for field in fields:
            print('%10s ' % (getattr(entry, field)), end="")
        print()

def create_formatter_orig(format):
    if format == 'text':
        return TextTableFormatter()
    elif format == 'csv':
        return CSVFormatter()
    elif format == 'html':
        return HTMLTableFormatter()
    else:
        raise ValueError('Unknown format %s' % format)