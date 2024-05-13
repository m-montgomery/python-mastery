import csv

class Stock:
    _types = (str, int, float)
    __slots__ = ('name', '_shares', '_price')

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __str__(self):
        return f"{self.shares} shares of {self.name} stock at price {self.price}"

    def __repr__(self):
        return f"Stock('{self.name}', {self.shares}, {self.price})"
    
    def __eq__(self, other):
        return isinstance(other, Stock) and self.name == other.name and self.shares == other.shares and self.price == other.price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)
    
    @classmethod
    def get_property_type(cls, property_name):
        entries = [pair for pair in zip(cls._types, cls.__slots__) if pair[1] == property_name]
        return entries[0][0] if any(entries) else None
    
    @classmethod
    def verify_property_type(cls, property_name, value):
        property_type = cls.get_property_type(property_name)
        if not isinstance(value, property_type):
            raise TypeError('Expected %s' % property_type.__name__)

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self.verify_property_type('_price', value)
        if value < 0:
            raise ValueError('Must be >= 0')

        self._price = value

    @property
    def shares(self):
        return self._shares
    
    @shares.setter
    def shares(self, value):
        self.verify_property_type('_shares', value)
        if value < 0:
            raise ValueError('Must be >= 0')

        self._shares = value

    @property
    def cost(self):
        return self.shares * self.price
    
    def sell(self, nshares):
        if nshares > self.shares:
            raise ValueError
        self.shares -= nshares


def read_portfolio(filename, cls=Stock):
    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)  # skip header
        for row in rows:
            #portfolio.append(Stock(row[0], int(row[1]), float(row[2])))
            portfolio.append(cls.from_row(row))
    return portfolio

def print_portfolio(portfolio):
    print('%10s %10s %10s' % ("name", "shares", "price"))
    print("---------- ---------- ----------")
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))
