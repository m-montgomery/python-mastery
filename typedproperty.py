# typedproperty.py

def typedproperty(expected_type):
    private_name = None

    @property
    def value(self):
        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f'Expected {expected_type}')
        setattr(self, private_name, val)

    def __set_name__(self, cls, name):
        private_name = '_' + name
   
    return value

def String():
    return typedproperty(str)

def Integer():
    return typedproperty(int)

def Float():
    return typedproperty(float)
