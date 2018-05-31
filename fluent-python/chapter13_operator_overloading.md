
## Operator Overloading 101
Operator overloading has a bad name in some circles. It is a language feature that can be (and has been) abused, resulting in programmer confusion, bugs, and unexpected performance bottlenecks. But if well used, it leads to pleasurable APIs and readable code. Python strikes a good balance between flexibility, usability, and safety by imposing some limitations:
* We cannot overload operators for the built-in types.
* We cannot create new operators, only overload existing ones.
* A few operators can’t be overloaded: is, and, or, not (but the bitwise &, |, ~, can).

## Unary Operators
In The Python Language Reference, “6.5. Unary arithmetic and bitwise operations” lists three unary operators, shown here with their associated special methods:
* \- (\__neg__)
Arithmetic unary negation. If x is -2 then -x == 2.
* \+ (\__pos__)
Arithmetic unary plus. Usually x == +x, but there are a few cases when that’s not true. See “When x and +x Are Not Equal” on page 373 if you’re curious.
* \~ (\__invert__)
Bitwise inverse of an integer, defined as ~x == -(x+1). If x is 2 then ~x == -3.
The Data Model” chapter of The Python Language Reference also lists the abs(...) built- in function as a unary operator. The associated special method is \__abs__, as we’ve seen before, starting with “Emulating Numeric Types” on page 9.

It’s easy to support the unary operators. Simply implement the appropriate special method, which will receive just one argument: self. Use whatever logic makes sense in your class, but stick to the fundamental rule of operators: always return a new object. In other words, do not modify self, but create and return a new instance of a suitable type.

In the case of - and +, the result will probably be an instance of the same class as self; for +, returning a copy of self is the best approach most of the time. For abs(...), the result should be a scalar number. As for ~, it’s difficult to say what would be a sensible result if you’re not dealing with bits in an integer, but in an ORM it could make sense to return the negation of an SQL WHERE clause, for example.


```python
# Example 13-1: unary operators - and + added to Example 10-16
import math
import itertools

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
        
    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))
    
    def __neq__(self):
        # To compute -v, build a new Vector with every component of self negated.
        return Vector(-x for x in self)
    
    def __pos__(self):
        # To compute +v, build a new Vector with every component of self.
        return Vector(self)
    
    def __add__(self, other):
        pairs = itertools.zip_longest(self, other, fillvalue=0.0)
        return Vector(a + b for a, b in pairs)
```

## Overloading + for Vector Addition
Adding two Euclidean vectors results in a new vector in which the components are the pairwise additions of the components of the addends. 

```python
# Example 13-4: Vector.add method
def __add__(self, other):
    pairs = itertools.zip_longest(self, other, fillvalue=0.0)
    return Vector(a + b for a, b in pairs)
```


```python
v1 = Vector([3, 4, 5])
v2 = Vector([4, 5, 6])
```


```python
v1 + v2
```




    (7, 9, 11)




```python
v3 = Vector([1])
v1 + v3
```




    (4, 4.0, 5.0)



To support operations involving objects of different types, Python implements a special dispatching mechanism for the infix operator special methods. Given an expression a + b, the interpreter will perform these steps (also see Figure 13-1):

* If a has \__add__, call a.\__add__(b) and return result unless it’s NotImplemented.
* If a doesn’t have \__add__, or calling it returns NotImplemented, check if b has \__radd__, then call b.\__radd__(a) and return result unless it’s NotImplemented.
* If b doesn’t have \__radd__, or calling it returns NotImplemented, raise TypeError with an unsupported operand types message.

The \__radd__ method is called the “reflected” or “reversed” version of \__add__. I prefer to call them “reversed” special methods. Three of this book’s technical reviewers—Alex, Anna, and Leo—told me they like to think of them as the “right” special methods, because they are called on the righthand operand. Whatever “r”-word you prefer, that’s what the “r” prefix stands for in \__radd__, \__rsub__, and the like.

Therefore, to make the mixed-type additions in Example 13-6 work, we need to imple‐ ment the Vector.\__radd__ method, which Python will invoke as a fall back if the left operand does not implement \__add__ or if it does but returns NotImplemented to signal that it doesn’t know how to handle the right operand.

```python
def __add__(self, other):
    pairs = itertools.zip_longest(self, other, fillvalue=0.0)
    return Vector(a + b for a, b in pairs)

# __radd__ just delegates to __add__.
def __radd__(self, other):
    return self + other
```

The problems in Examples 13-8 and 13-9 actually go deeper than obscure error mes‐ sages: if an operator special method cannot return a valid result because of type incom‐ patibility, it should return NotImplemented and not raise TypeError. By returning NotImplemented, you leave the door open for the implementer of the other operand type to perform the operation when Python tries the reversed method call.

In the spirit of duck typing, we will refrain from testing the type of the other operand, or the type of its elements. We’ll catch the exceptions and return NotImplemented. If the interpreter has not yet reversed the operands, it will try that. If the reverse method call returns NotImplemented, then Python will raise issue TypeError with a standard error message like “unsupported operand type(s) for +: Vector and str.”

The final implementation of the special methods for Vector addition are in Example 13-10.

```python
# Example 13-10: operator + methods added
def __add__(self, other):
    try:
        pairs = itertools.zip_longest(self, other, fillvalue=0.0)
        return Vector(a + b for a, b in pairs)
    except TypeError:
        return NotImplemented

def __radd__(self, other):
    return self + other
```

## Overloading * for Scalar Multiplication
What does Vector([1, 2, 3]) * x mean? If x is a number, that would be a scalar product, and the result would be a new Vector with each component multiplied by x— also known as an elementwise multiplication;

Another kind of product involving Vector operands would be the dot product of two vectors—or matrix multiplication, if you take one vector as a 1 × N matrix and the other as an N × 1 matrix. The current practice in NumPy and similar libraries is not to overload the * with these two meanings, but to use * only for the scalar product. For example, in NumPy, numpy.dot() computes the dot product.


```python
# Exmaple 13-11: operator * method added
from array import array
import reprlib
import math
import functools
import operator
import itertools
import numbers

class Vector:
    typecode = 'd'
    
    def __init__(self, components):
        self._components = array(self.typecode, components)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        else:
            return self._components[index]
        
    def __repr__(self):
        return str(tuple(self._components))
        
    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        else:
            return NotImplemented
        
    def __rmul__(self, scalar):
        return self * scalar
```


```python
v1 = Vector([1, 2, 3])
v1 * 10
```




    (10.0, 20.0, 30.0)




```python
11 * v1
```




    (11.0, 22.0, 33.0)




```python
v1 * True
```




    (1.0, 2.0, 3.0)




```python
from fractions import Fraction
v1 * Fraction(1, 3)
```




    (0.3333333333333333, 0.6666666666666666, 1.0)



## Rick Comparison Operators
The handling of the rich comparison operators ==, !=, >, <, >=, <= by the Python inter‐ preter is similar to what we just saw, but differs in two important aspects:
* The same set of methods are used in forward and reverse operator calls. The rules are summarized in Table 13-2. For example, in the case of==, both the forward and reverse calls invoke \__eq__, only swapping arguments; and a forward call to \__gt__ is followed by a reverse call to \__lt__ with the swapped arguments.
* In the case of == and !=, if the reverse call fails, Python compares the object IDs instead of raising TypeError.


```python
# Exmaple 13-12: operator * method added
from array import array
import reprlib
import math
import functools
import operator
import itertools
import numbers

class Vector:
    typecode = 'd'
    
    def __init__(self, components):
        self._components = array(self.typecode, components)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        else:
            return self._components[index]
        
    def __repr__(self):
        return str(tuple(self._components))
        
    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        else:
            return NotImplemented
        
    def __rmul__(self, scalar):
        return self * scalar
    
    def __len__(self):
        return len(self._components)
    
    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))
```


```python
va = Vector([1.0, 2.0, 3.0, 4.0])
vb = Vector(range(1, 5))
va == vb
```




    True




```python
va == (1, 2, 3, 4)
```




    True



Taking a clue from Python itself, we can see that [1,2] == (1, 2) is False. Therefore, let’s be conservative and do some type checking. If the second operand is a Vector instance (or an instance of a Vector subclass), then use the same logic as the current \__eq__. Otherwise, return NotImplemented and let Python handle that.


```python
# Exmaple 13-13: operator * method added
from array import array
import reprlib
import math
import functools
import operator
import itertools
import numbers

class Vector:
    typecode = 'd'
    
    def __init__(self, components):
        self._components = array(self.typecode, components)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        else:
            return self._components[index]
        
    def __repr__(self):
        return str(tuple(self._components))
        
    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        else:
            return NotImplemented
        
    def __rmul__(self, scalar):
        return self * scalar
    
    def __len__(self):
        return len(self._components)
    
    def __eq__(self, other):
        if isinstance(other, Vector):
            return (len(self) == len(other) and
                    all(a == b for a, b in zip(self, other)))
        else:
            return NotImplemented
```


```python
va = Vector([1.0, 2.0, 3.0])
vb = Vector(range(1, 4))
va == vb
```




    True




```python
t3 = (1, 2, 3)
va == t3
```




    False



As for the comparison between Vector and tuple in Example 13-14, the actual steps are:
1. To evaluate va == t3, Python calls Vector.\__eq__(va, t3).
2. Vector.\__eq__(va, t3) verifies that t3 is not a Vector and returns NotImplemen
ted.
3. Python gets NotImplemented result, so it tries tuple.\__eq__(t3, va).
4. tuple.\__eq__(t3, va) has no idea what a Vector is, so it returns NotImplemented.
5. In the special case of ==, if the reversed call returns NotImplemented, Python com‐ pares object IDs as a last resort.

How about !=? We don’t need to implement it because the fallback behavior of the \__ne__ inherited from object suits us: when \__eq__ is defined and does not return NotImplemented, \__ne__ returns that result negated.


```python
va != vb
```




    False




```python
va != (1, 2, 3)
```




    True



The \__ne__ inherited from object works like the following code—except that the orig‐ inal is written in C:

```python
def __ne__(self, other):
    eq_result = self == other
    if eq_result is NotImplemented:
        return NotImplemented
    else:
        return not eq_result
```

## Augmented Assignment Operators
If a class does not implement the in-place operators listed in Table 13-1, the augmented assignment operators are just syntactic sugar: a += b is evaluated exactly as a = a + b. That’s the expected behavior for immutable types, and if you have \__add__ then += will work with no additional code.

However, if you do implement an in-place operator method such as \__iadd__, that method is called to compute the result of a += b. As the name says, those operators are expected to change the lefthand operand in place, and not create a new object as the result.
