
## Object Representations
Every object-oriented language has at least one standard way of getting a string repre‐ sentation from any object. 

Python has two:
* repr()
Return a string representing the object as the developer wants to see it.
* str()
Return a string representing the object as the user wants to see it.

As you know, we implement the special methods __repr__ and __str__ to support
repr() and str().

There are two additional special methods to support alternative representations of ob‐ jects: \__bytes__ and \__format__. The \__bytes__ method is analogous to \__str__: it’s called by bytes() to get the object represented as a byte sequence. Regarding \__format__, both the built-in function format() and the str.format() method call it to get string displays of objects using special formatting codes. We’ll cover \__bytes__ in the next example, and \__format__ after that.

## Vector Class Redux


```python
# Example 9-2: Vector2d define
from array import array
import math

class Vector2d:
    # typecode is a class attribute we’ll use when converting Vector2d instances to/from bytes.
    typecode = 'd'
    
    def __init__(self, x, y):
        # Converting x and y to float in __init__ catches errors early,
        # which is helpful in case Vector2d is called with unsuitable arguments.
        self.x = float(x)
        self.y = float(y)
        
    def __iter__(self):
        # __iter__ makes a Vector2d iterable; this is what makes unpacking work (e.g, x, y = my_vector). 
        # We implement it simply by using a generator expression to yield the components one after the other.
        return (i for i in (self.x, self.y))
    
    def __repr__(self):
        class_name = type(self).__name__
        # __repr__ builds a string by interpolating the components with {!r} to get their repr;
        # because Vector2d is iterable, *self feeds the x and y components to format.
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self):
        # From an iterable Vector2d, it’s easy to build a tuple for display as an ordered pair.
        return str(tuple(self))
    
    def __bytes__(self):
        # To generate bytes, we convert the typecode to bytes and concatenate...
        # ...bytes converted from an array built by iterating over the instance.
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
    
    def __eq__(self, other):
        # To quickly compare all components, build tuples out of the operands.
        # This works for operands that are instances of Vector2d, but has issues.
        # See the following warning.
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        # The magnitude is the length of the hypotenuse of the triangle formed by the x and y components.
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        # _bool__ uses abs(self) to compute the magnitude, then converts it to bool,
        # so 0.0 becomes False, nonzero is True.
        return bool(abs(self))
```


```python
# Example 9-1: Vector2d instances have several representations
v1 = Vector2d(3, 4)
```


```python
print(v1.x, v1.y)
```

    3.0 4.0



```python
x, y = v1
```


```python
x, y
```




    (3.0, 4.0)




```python
v1
```




    Vector2d(3.0, 4.0)




```python
str(v1)
```




    '(3.0, 4.0)'




```python
print(v1)
```

    (3.0, 4.0)



```python
v1_clone = eval(repr(v1))
```


```python
v1_clone == v1
```




    True




```python
octects = bytes(v1)
```


```python
octects
```




    b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'




```python
abs(v1)
```




    5.0




```python
bool(v1), bool(Vector2d(0, 0))
```




    (True, False)



## An Alternative Constructor


```python
# Example 9-3. Part of vector2d_v1.py: this snippet shows only the frombytes class meth‐ od,
# added to the Vector2d definition
from array import array
import math

class Vector2d:
    # typecode is a class attribute we’ll use when converting Vector2d instances to/from bytes.
    typecode = 'd'
    
    def __init__(self, x, y):
        # Converting x and y to float in __init__ catches errors early,
        # which is helpful in case Vector2d is called with unsuitable arguments.
        self.x = float(x)
        self.y = float(y)
        
    def __iter__(self):
        # __iter__ makes a Vector2d iterable; this is what makes unpacking work (e.g, x, y = my_vector). 
        # We implement it simply by using a generator expression to yield the components one after the other.
        return (i for i in (self.x, self.y))
    
    def __repr__(self):
        class_name = type(self).__name__
        # __repr__ builds a string by interpolating the components with {!r} to get their repr;
        # because Vector2d is iterable, *self feeds the x and y components to format.
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self):
        # From an iterable Vector2d, it’s easy to build a tuple for display as an ordered pair.
        return str(tuple(self))
    
    def __bytes__(self):
        # To generate bytes, we convert the typecode to bytes and concatenate...
        # ...bytes converted from an array built by iterating over the instance.
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
    
    def __eq__(self, other):
        # To quickly compare all components, build tuples out of the operands.
        # This works for operands that are instances of Vector2d, but has issues.
        # See the following warning.
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        # The magnitude is the length of the hypotenuse of the triangle formed by the x and y components.
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        # _bool__ uses abs(self) to compute the magnitude, then converts it to bool,
        # so 0.0 becomes False, nonzero is True.
        return bool(abs(self))
    
    # Class method is modified by the classmethod decorator.
    @classmethod
    # No self argument; instead, the class itself is passed as cls.
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
    
    # Example 9.5: implements __format__ to produce the displays just shown
    def __format__(self, fmt_spec=''):
        # Use the format built-in to apply the fmt_spec to each vector component,
        # building an iterable of formatted strings.
        components = (format(c, fmt_spec) for c in self)
        # Plug the formatted strings in the formula '(x, y)'.
        return '({}, {})'.format(*components)
```

## classmethod Versus staticmethod
The classmethod decorator is not mentioned in the Python tutorial, and neither is staticmethod. Anyone who has learned OO in Java may wonder why Python has both of these decorators and not just one of them.

Let’s start with classmethod. Example 9-3 shows its use: to define a method that operates on the class and not on instances. classmethod changes the way the method is called, so it receives the class itself as the first argument, instead of an instance. Its most com‐ mon use is for alternative constructors, like frombytes in Example 9-3. Note how the last line of frombytes actually uses the cls argument by invoking it to build a new instance: cls(*memv). By convention, the first parameter of a class method should be named cls (but Python doesn’t care how it’s named).

In contrast, the staticmethod decorator changes a method so that it receives no special first argument. In essence, a static method is just like a plain function that happens to live in a class body, instead of being defined at the module level. Example 9-4 contrasts the operation of classmethod and staticmethod.


```python
# Example 9-4: Comparing behaviors of classmethod and staticmethod
class Demo:
    
    @classmethod
    def klassmeth(*args):
        return args
    
    @staticmethod
    def statmeth(*args):
        return args
```


```python
Demo.klassmeth()
```




    (__main__.Demo,)




```python
# No matter how you invoke it, Demo.klassmeth receives the Demo class as the first argument.
Demo.klassmeth('spam')
```




    (__main__.Demo, 'spam')




```python
# Demo.statmeth behaves just like a plain old function.
Demo.statmeth()
```




    ()




```python
Demo.statmeth('spam')
```




    ('spam',)



## Formatted Displays
The format() built-in function and the str.format() method delegate the actual for‐ matting to each type by calling their .\__format__(format_spec) method. The for mat_spec is a formatting specifier, which is either:
* The second argument in format(my_obj, format_spec), or
* Whatever appears after the colon in a replacement field delimited with {} inside a
format string used with str.format()


```python
brl = 1/2.43
brl
```




    0.4115226337448559




```python
format(brl, '0.4f')
```




    '0.4115'




```python
'{:0.4f}'.format(brl)
```




    '0.4115'



The Format Specification Mini-Language is extensible because each class gets to inter‐ pret the format_spec argument as it likes. For instance, the classes in the datetime module use the same format codes in the strftime() functions and in their \__format__ methods. Here are a couple examples using the format() built-in and the str.format() method:


```python
from datetime import datetime
now = datetime.now()
format(now, '%H:%M:%S')
```




    '15:53:19'




```python
"It's now {:%I:%M %p}".format(now)
```




    "It's now 03:53 PM"



If a class has no \__format__, the method inherited from object returns str(my_ob ject). Because Vector2d has a \__str__, this works:


```python
v1 = Vector2d(3, 4)
format(v1)
```




    '(3.0, 4.0)'



However, if you pass a format specifier, object.\__format__ raises TypeError:


```python
format(v1, '.3f')
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-35-9f7764dc3848> in <module>()
    ----> 1 format(v1, '.3f')
    

    TypeError: unsupported format string passed to Vector2d.__format__



```python
# Example 9-5
v1 = Vector2d(3, 4)
format(v1)
```




    '(3.0, 4.0)'




```python
format(v1, '.2f')
```




    '(3.00, 4.00)'




```python
format(v1, '.3e')
```




    '(3.000e+00, 4.000e+00)'




```python
# Example 9-6
class Vector2d:
    # typecode is a class attribute we’ll use when converting Vector2d instances to/from bytes.
    typecode = 'd'
    
    def __init__(self, x, y):
        # Converting x and y to float in __init__ catches errors early,
        # which is helpful in case Vector2d is called with unsuitable arguments.
        self.x = float(x)
        self.y = float(y)
        
    def __iter__(self):
        # __iter__ makes a Vector2d iterable; this is what makes unpacking work (e.g, x, y = my_vector). 
        # We implement it simply by using a generator expression to yield the components one after the other.
        return (i for i in (self.x, self.y))
    
    def __repr__(self):
        class_name = type(self).__name__
        # __repr__ builds a string by interpolating the components with {!r} to get their repr;
        # because Vector2d is iterable, *self feeds the x and y components to format.
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self):
        # From an iterable Vector2d, it’s easy to build a tuple for display as an ordered pair.
        return str(tuple(self))
    
    def __bytes__(self):
        # To generate bytes, we convert the typecode to bytes and concatenate...
        # ...bytes converted from an array built by iterating over the instance.
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
    
    def __eq__(self, other):
        # To quickly compare all components, build tuples out of the operands.
        # This works for operands that are instances of Vector2d, but has issues.
        # See the following warning.
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        # The magnitude is the length of the hypotenuse of the triangle formed by the x and y components.
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        # _bool__ uses abs(self) to compute the magnitude, then converts it to bool,
        # so 0.0 becomes False, nonzero is True.
        return bool(abs(self))
    
    # Class method is modified by the classmethod decorator.
    @classmethod
    # No self argument; instead, the class itself is passed as cls.
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
    
    def angle(self):
        return math.atan2(self.y, self.x)
    
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)
```


```python
format(Vector2d(1, 1), 'p')
```




    '<1.4142135623730951, 0.7853981633974483>'




```python
format(Vector2d(1, 1), '.3ep')
```




    '<1.414e+00, 7.854e-01>'




```python
format(Vector2d(1, 1), '.5fp')
```




    '<1.41421, 0.78540>'



## A Hasable Vector2d
As defined, so far our Vector2d instances are unhashable, so we can’t put them in a set:


```python
v1 = Vector2d(3, 4)
hash(v1)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-48-293f2e233a24> in <module>()
          1 v1 = Vector2d(3, 4)
    ----> 2 hash(v1)
    

    TypeError: unhashable type: 'Vector2d'



```python
set([v1])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-49-bc2432ceb71f> in <module>()
    ----> 1 set([v1])
    

    TypeError: unhashable type: 'Vector2d'


To make a Vector2d hashable, we must implement \__hash__ (\__eq__ is also required, and we already have it). We also need to make vector instances immutable, as we’ve seen in “What Is Hashable?” on page 65.


```python
# Example 9-7: only the changes needed to make Vector2d immutable are shown here;
class Vector2d:
    typecode = 'd'
    
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)
        
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __iter__(self):
        return (i for i in (self.x, self.y))
```


```python
v1 = Vector2d(3, 4)
```


```python
v1.x = 7
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-63-a24b78470952> in <module>()
    ----> 1 v1.x = 7
    

    AttributeError: can't set attribute



```python
v1._x
```




    3.0



Now that our vectors are reasonably immutable, we can implement the \__hash__ method. It should return an int and ideally take into account the hashes of the object attributes that are also used in the \__eq__ method, because objects that compare equal should have the same hash. The __hash__ special method documentation suggests using the bitwise XOR operator (^) to mix the hashes of the components, so that’s what we do. The code for our Vector2d.\__hash__ method is really simple, as shown in Example 9-8.


```python
# Example 9.8: implementation of hash
class Vector2d:
    typecode = 'd'
    
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)
        
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __iter__(self):
        return (i for i in (self.x, self.y))
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
```


```python
v1 = Vector2d(3, 4)
v2 = Vector2d(3.1, 4.2)
```


```python
hash(v1), hash(v2)
```




    (283411527, -9223372036571364201)




```python
set([v1, v2])
```




    {<__main__.Vector2d at 0x10e484470>, <__main__.Vector2d at 0x10e484978>}



If you are creating a type that has a sensible scalar numeric value, you may also imple‐ ment the \__int__ and \__float__ methods, invoked by the int() and float() con‐ structors—which are used for type coercion in some contexts. There’s also a \__complex__ method to support the complex() built-in constructor. Perhaps Vector2d should provide \__complex__, but I’ll leave that as an exercise for you.

We have been working on Vector2d for a while, showing just snippets, so Example 9-9 is a consolidated, full listing of vector2d_v3.py, including all the doctests I used when developing it.


```python
# Example 9-9: the full monty
from array import array
import math

class Vector2d:
    typecode = 'd'
    
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __iter__(self):
        return (i for i in (self.x, self.y))
    
    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
    
    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self))
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
    
    def angle(self):
        return math.atan2(self.y, self.x)
    
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)
```

## Private and "Protected" Attributes in Python
n Python, there is no way to create private variables like there is with the private modifier in Java. What we have in Python is a simple mechanism to prevent accidental overwriting of a “private” attribute in a subclass.

Consider this scenario: someone wrote a class named Dog that uses a mood instance attribute internally, without exposing it. You need to subclass Dog as Beagle. If you create your own mood instance attribute without being aware of the name clash, you will clobber the mood attribute used by the methods inherited from Dog. This would be a pain to debug.

To prevent this, if you name an instance attribute in the form \__mood (two leading underscores and zero or at most one trailing underscore), Python stores the name in the instance \__dict__ prefixed with a leading underscore and the class name, so in the Dog class, \__mood becomes _Dog__mood, and in Beagle it’s _Beagle__mood. This language feature goes by the lovely name of name mangling.



```python
class Vector2d:
    
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
```


```python
v1 = Vector2d(3, 4)
v1
```




    <__main__.Vector2d at 0x10e484320>




```python
v1.__x
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-74-e16dadf2437c> in <module>()
    ----> 1 v1.__x
    

    AttributeError: 'Vector2d' object has no attribute '__x'



```python
# Name mangling to directly access the private attribute
v1._Vector2d__x
```




    3.0



Anyone who knows how private names are mangled can read the private attribute di‐ rectly, as the last line of Example 9-10 shows—that’s actually useful for debugging and serialization. They can also directly assign a value to a private component of a Vector2d by simply writing v1._Vector__x = 7. But if you are doing that in production code, you can’t complain if something blows up.

The name mangling functionality is not loved by all Pythonistas, and neither is the skewed look of names written as self.__x. Some prefer to avoid this syntax and use just one underscore prefix to “protect” attributes by convention (e.g., self._x). Critics of the automatic double-underscore mangling suggest that concerns about accidental attribute clobbering should be addressed by naming conventions. This is the full quote from the prolific Ian Bicking, cited at the beginning of this chapter:

The single underscore prefix has no special meaning to the Python interpreter when used in attribute names, but it’s a very strong convention among Python programmers that you should not access such attributes from outside the class.8 It’s easy to respect the privacy of an object that marks its attributes with a single _, just as it’s easy respect the convention that variables in ALL_CAPS should be treated as constants.

Attributes with a single _ prefix are called “protected” in some corners of the Python documentation.9 The practice of “protecting” attributes by convention with the form self._x is widespread, but calling that a “protected” attribute is not so common. Some even call that a “private” attribute.

To conclude: the Vector2d components are “private” and our Vector2d instances are “immutable”—with scare quotes—because there is no way to make them really private and immutable.10

## Saving Space with the __slots__ Class Attribute
By default, Python stores instance attributes in a per-instance dict named \__dict__. As we saw in “Practical Consequences of How dict Works” on page 90, dictionaries have a significant memory overhead because of the underlying hash table used to provide fast access. If you are dealing with millions of instances with few attributes, the \__slots__ class attribute can save a lot of memory, by letting the interpreter store the instance attributes in a tuple instead of a dict.

To define __slots__, you create a class attribute with that name and assign it an iterable of str with identifiers for the instance attributes. I like to use a tuple for that, because it conveys the message that the __slots__ definition cannot change. See Example 9-11.


```python
# Example 9-11: the slots attribute
class Vector2d:
    __slots__ = ('__x', '__y')
    
    typecode = 'd'
    
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
```

By defining \__slots__ in the class, you are telling the interpreter: “These are all the instance attributes in this class.” Python then stores them in a tuple-like structure in each instance, avoiding the memory overhead of the per-instance \__dict__. This can make a huge difference in memory usage if your have millions of instances active at the same time.

### The problem with \__slots__
To summarize, __slots__ may provide significant memory savings if properly used, but there are a few caveats:
* You must remember to redeclare \__slots__ in each subclass, because the inherited attribute is ignored by the interpreter.
* Instances will only be able to have the attributes listed in \__slots__, unless you include '\__dict__' in \__slots__ (but doing so may negate the memory savings).
* Instances cannot be targets of weak references unless you remember to include '\__weakref__' in \__slots__.
