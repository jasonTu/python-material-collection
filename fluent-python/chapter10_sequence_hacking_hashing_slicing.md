
## Vector Take #1: Vector2d Compatible


```python
# Exmaple 10-2: Vector definition
from array import array
import reprlib
import math

class Vector:
    typecode = 'b'
    
    def __init__(self, components):
        self._components = array(self.typecode, components)
        
    def __iter__(self):
        return iter(self._components)
    
    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))
    
    def __bool__(self):
        return bool(abs(self))
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
```


```python
# Example 10-1: Tests of the Vector
Vector([3, 4])
```




    Vector([3, 4])




```python
Vector((3, 4, 5))
```




    Vector([3, 4, 5])




```python
Vector(range(10))
```




    Vector([0, 1, 2, 3, 4, ...])



## Protocols and Duck Typing
As early as Chapter 1, we saw that you don’t need to inherit from any special class to create a fully functional sequence type in Python; you just need to implement the meth‐ ods that fulfill the sequence protocol. But what kind of protocol are we talking about?

In the context of object-oriented programming, a protocol is an informal interface, defined only in documentation and not in code. For example, the sequence protocol in Python entails just the \__len__ and \__getitem__ methods. Any class Spam that imple‐ ments those methods with the standard signature and semantics can be used anywhere a sequence is expected. Whether Spam is a subclass of this or that is irrelevant; all that matters is that it provides the necessary methods. We saw that in Example 1-1, repro‐ duced here in Example 10-3.


```python
# Example 10-3: Code from Example 1-1
import collections

Card = collections.namedtuple('Card', 'rank suit')

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self._suits
                      for rank in self._ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
```

The FrenchDeck class in Example 10-3 takes advantage of many Python facilities because it implements the sequence protocol, even if that is not declared anywhere in the code. Any experienced Python coder will look at it and understand that it is a sequence, even if it subclasses object. We say it is a sequence because it behaves like one, and that is what matters.

This became known as duck typing, after Alex Martelli’s post quoted at the beginning of this chapter.
Because protocols are informal and unenforced, you can often get away with imple‐ menting just part of a protocol, if you know the specific context where a class will be used. For example, to support iteration, only \__getitem__ is required; there is no need to provide \__len__.

## Vector Take #2: A Sliceable Sequence
As we saw with the FrenchDeck example, supporting the sequence protocol is really easy if you can delegate to a sequence attribute in your object, like our self._components array. These \__len__ and \__getitem__ one-liners are a good start:


```python
class Vector:
    # many lines omitted
    # ...
    def __init__(self, components):
        self._components = components
        
    def __len__(self):
        return len(self._components)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        else:
            return self._components[index]
    
    def __repr__(self):
        return str(tuple(self._components))
```


```python
v1 = Vector([3, 4, 5])
len(v1)
```




    3




```python
v1[0], v1[1]
```




    (3, 4)




```python
v7 = Vector(range(7))
```


```python
v7[1:4]
```




    (1, 2, 3)



### How Slicing Works


```python
# Example 10-4: Checking out the behavior of __getitem__ and slices
class MySeq:
    def __getitem__(self, index):
        return index
```


```python
s = MySeq()
```


```python
s[1]
```




    1




```python
s[1:4]
```




    slice(1, 4, None)




```python
s[1:4:2]
```




    slice(1, 4, 2)




```python
s[1:4:2, 9]
```




    (slice(1, 4, 2), 9)




```python
s[1:4:2, 7:9]
```




    (slice(1, 4, 2), slice(7, 9, None))




```python
# Example 10-5: Inspecting the attributes of the slice class
slice
```




    slice




```python
dir(slice)
```




    ['__class__',
     '__delattr__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__le__',
     '__lt__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     'indices',
     'start',
     'step',
     'stop']




```python
help(slice.indices)
```

    Help on method_descriptor:
    
    indices(...)
        S.indices(len) -> (start, stop, stride)
        
        Assuming a sequence of length len, calculate the start and stop
        indices, and the stride length of the extended slice described by
        S. Out of bounds indices are clipped in a manner consistent with the
        handling of normal slices.
    


In other words, indices exposes the tricky logic that’s implemented in the built-in sequences to gracefully handle missing or negative indices and slices that are longer than the target sequence. This method produces “normalized” tuples of nonnegative start, stop, and stride integers adjusted to fit within the bounds of a sequence of the given length.


```python
slice(None, 10, 2).indices(5)
```




    (0, 5, 2)




```python
slice(-3, None, None).indices(5)
```




    (2, 5, 1)



### A Slice-Aware __getitem__
```python
def __getitem__(self, index):
    cls = type(self)
    if isinstance(index, slice):
        return cls(self._components[index])
    elif isinstance(index, numbers.Integral):
        return self._components[index]
    else:
        msg = '{cls.__name__} indices must be integers'
        raise TypeError(msg.format(cls=cls))
```

## Vector Take #3: Dynamic Attribute Access
In the evolution from Vector2d to Vector, we lost the ability to access vector compo‐ nents by name (e.g., v.x, v.y). We are now dealing with vectors that may have a large number of components. Still, it may be convenient to access the first few components with shortcut letters such as x, y, z instead of v[0], v[1] and v[2].

Here is the alternative syntax we want to provide for reading the first four components of a vector:

```python
v = Vector(range(10))
v.x
v.y, v.z, v.t
```

In Vector2d, we provided read-only access to x and y using the @property decorator (Example 9-7). We could write four properties in Vector, but it would be tedious. The __getattr__ special method provides a better way.

“The \__getattr__ method is invoked by the interpreter when attribute lookup fails. In simple terms, given the expression my_obj.x, Python checks if the my_obj instance has an attribute named x; if not, the search goes to the class (my_obj.\__class__), and then up the inheritance graph.2 If the x attribute is not found, then the \__getattr__ method defined in the class of my_obj is called with self and the name of the attribute as a string (e.g., 'x').


```python
# Example 10-8: __getattr__ method added to Vector class
class Vector:
    # many lines omitted
    # ...
    def __init__(self, components):
        self._components = components
        
    def __len__(self):
        return len(self._components)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        else:
            return self._components[index]
    
    def __repr__(self):
        return str(tuple(self._components))
    
    shortcut_names = 'xyzt'
    
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name!__r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))
```


```python
v = Vector(range(5))
v
```




    (0, 1, 2, 3, 4)




```python
v.x
```




    0




```python
v.x = 10
```


```python
v.x
```




    10




```python
v
```




    (0, 1, 2, 3, 4)



Can you explain what is happening? In particular, why the second time v.x returns 10 if that value is not in the vector components array? If you don’t know right off the bat, study the explanation of \__getattr__ given right before Example 10-8. It’s a bit subtle, but a very important foundation to understand a lot of what comes later in the book.

The inconsistency in Example 10-9 was introduced because of the way \__getattr__ works: Python only calls that method as a fall back, when the object does not have the named attribute. However, after we assign v.x = 10, the v object now has an x attribute, so \__getattr__ will no longer be called to retrieve v.x: the interpreter will just return the value 10 that is bound to v.x. On the other hand, our implementation of \__getattr__ pays no attention to instance attributes other than self._components, from where it retrieves the values of the “virtual attributes” listed in shortcut_names.

We need to customize the logic for setting attributes in our Vector class in order to avoid this inconsistency.

Recall that in the latest Vector2d examples from Chapter 9, trying to assign to the .x or .y instance attributes raised AttributeError. In Vector we want the same exception with any attempt at assigning to all single-letter lowercase attribute names, just to avoid confusion. To do that, we’ll implement __setattr__ as listed in Example 10-10.


```python
# Example 10-10: __setattr__ method in Vector class
class Vector:
    # many lines omitted
    # ...
    def __init__(self, components):
        self._components = components
        
    def __len__(self):
        return len(self._components)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        else:
            return self._components[index]
    
    def __repr__(self):
        return str(tuple(self._components))
    
    shortcut_names = 'xyzt'
    
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name!__r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))
    
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)
```


```python
v1 = Vector(range(5))
v1
```




    (0, 1, 2, 3, 4)




```python
v1.x
```




    0




```python
v1.x = 1
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-91-cc7291a3118c> in <module>()
    ----> 1 v1.x = 1
    

    <ipython-input-88-1dcf97a42734> in __setattr__(self, name, value)
         41             if error:
         42                 msg = error.format(cls_name=cls.__name__, attr_name=name)
    ---> 43                 raise AttributeError(msg)
         44         super().__setattr__(name, value)


    AttributeError: readonly attribute x



```python
v1.aa = 2
```


```python
v1.aa
```




    2



Even without supporting writing to the Vector components, here is an important take‐ away from this example: very often when you implement \__getattr__ you need to code \__setattr__ as well, to avoid inconsistent behavior in your objects.

If we wanted to allow changing components, we could implement \__setitem__ to en‐ able v[0] = 1.1 and/or \__setattr__ to make v.x = 1.1 work. But Vector will remain immutable because we want to make it hashable in the coming section.

## Vector Take #4: Hashing and a Faster ==
Once more we get to implement a \__hash__ method. Together with the existing \__eq__, this will make Vector instances hashable.

The \__hash__ in Example 9-8 simply computed hash(self.x) ^ hash(self.y). We now would like to apply the ^ (xor) operator to the hashes of every component, in succession, like this: v[0] ^ v[1] ^ v[2].... That is what the functools.reduce function is for. Previously I said that reduce is not as popular as before,3 but computing the hash of all vector components is a perfect job for it. Figure 10-1 depicts the general idea of the reduce function.


```python
# Example 10-11: Three ways of calculating the accumulated xor of integers from 0 to 5
n = 0
for i in range(1, 6):
    n ^= i
n
```




    1




```python
import functools
functools.reduce(lambda a, b: a^b, range(6))
```




    1




```python
import operator
functools.reduce(operator.xor, range(6))
```




    1




```python
# Example 10-12: two imports and __hash__ method added
from array import array
import reprlib
import math
import functools
import operator

class Vector:
    typecode = 'd'
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashed, 0)
```


```python
# Example 10-13: using zip in a for loop for more efficient comparison
def __eq__(self, other):
    if len(self) != len(other):
        return False
    for a, b in zip(self, other):
        if a != b:
            return False
    return True
```


```python
# Example 10-14: using zip and all
def __eq__(self, other):
    return len(self) == len(other) and all(a == b for a, b in zip(self, other))
```

## Vector Take #5: Formatiting

```python
def __format__(selfm fmt_spec=''):
    if fmt_spec.endswith('h'):
        fmt_spec = fmt_spec[:-1]
        coords = itertools.chain([abs(self)], self.angles())
        outer_fmt = '<{}>'
    else:
        coords = self
        outer_fmt = '({})'
    components = (format(c, fmt_spec) for c in coords)
    return outer_fmt.format(', '.join(components)
```
