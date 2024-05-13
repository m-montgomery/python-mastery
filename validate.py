# validate.py
class Validator:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)

class Typed(Validator):
    expected_type = object
    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type}')
        return super().check(value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass

class Stock:
    name   = String()
    shares = PositiveInteger()
    price  = PositiveFloat()

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
    
    @property
    def cost(self):
        return self.shares * self.price
    
    def sell(self, nshares):
        PositiveInteger.check(nshares)
        if nshares > self.shares:
            raise ValueError
        self.shares -= nshares
