## Dive into Python Decriptor

```python
# coding: utf-8

from weakref import WeakKeyDictionary

class NonNegative(object):
    def __init__(self, default):
        self.default = default
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Negative value not allowed: %s' % value)
        self.data[instance] = value


class Movie(object):
    rating = NonNegative(0)
    runtime = NonNegative(0)
    budget = NonNegative(0)
    grass = NonNegative(0)

    def __init__(self, title, rating, runtime, budget, grass):
        self.title = title
        self.rating = rating
        self.budget = budget
        self.grass = grass

    def profit(self):
        return self.grass - self.budget


m = Movie('Casablanca', 97, 102, 964000, 1300000)
print m.budget
m.rating = 100
try:
    m.rating = -1
except ValueError:
    print 'Woops, negative value'

```
