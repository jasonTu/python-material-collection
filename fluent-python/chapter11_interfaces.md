
## Interfaces and Protocols in Python Culture


```python
# Example 11-3: Partial sequence protocol implementation with __getitem__;
# enough for item access, iteration and the in operator
class Foo:
    def __getitem__(self, pos):
        return range(0, 30, 10)[pos]
```


```python
f = Foo()
f[1]
```




    10




```python
for i in f: print(i)
```

    0
    10
    20



```python
20 in f
```




    True




```python
15 in f
```




    False



There is no method \__iter__ yet Foo instances are iterable because—as a fallback— when Python sees a \__getitem__ method, it tries to iterate over the object by calling that method with integer indexes starting with 0. Because Python is smart enough to iterate over Foo instances, it can also make the in operator work even if Foo has no \__contains__ method: it does a full scan to check if an item is present.

In summary, given the importance of the sequence protocol, in the absence \__iter__ and \__contains__ Python still manages to make iteration and the in operator work by invoking \__getitem__.


```python
# Example 11-4: A deck as a sequence of cards
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
```

## Monkey-Patching to Implement a Protocol at Runtime
The FrenchDeck class from Example 11-4 has a major flaw: it cannot be shuffled. Years ago when I first wrote the FrenchDeck example I did implement a shuffle method. Later I had a Pythonic insight: if a FrenchDeck acts like a sequence, then it doesn’t need its own shuffle method because there is already random.shuffle, documented as “Shuffle the sequence x in place.”


```python
from random import shuffle
l = list(range(10))
shuffle(l)
l
```




    [1, 6, 2, 5, 3, 7, 4, 9, 8, 0]



However, if we try to shuffle a FrenchDeck instance, we get an exception, as in Example 11-5.


```python
# Example 11-5: random.shuffle cannot handle FrenchDeck
from random import shuffle
deck = FrenchDeck()
shuffle(deck)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-13-c48747a338b4> in <module>()
          2 from random import shuffle
          3 deck = FrenchDeck()
    ----> 4 shuffle(deck)
    

    ~/pyenv/ml/lib/python3.6/random.py in shuffle(self, x, random)
        273                 # pick an element in x[:i+1] with which to exchange x[i]
        274                 j = randbelow(i+1)
    --> 275                 x[i], x[j] = x[j], x[i]
        276         else:
        277             _int = int


    TypeError: 'FrenchDeck' object does not support item assignment


The error message is quite clear: “'FrenchDeck' object does not support item assign‐ ment.” The problem is that shuffle operates by swapping items inside the collection, and FrenchDeck only implements the immutable sequence protocol. Mutable sequences must also provide a \__setitem__ method.

Because Python is dynamic, we can fix this at runtime, even at the interactive console. Example 11-6 shows how to do it.


```python
# Example 11-6: Monkey patching FrenchDeck to make it mutable and compatible with random.shuffle
def set_card(deck, position, card):
    deck._cards[position] = card

FrenchDeck.__setitem__ = set_card
shuffle(deck)
deck[:5]
```




    [Card(rank='3', suit='diamonds'),
     Card(rank='8', suit='clubs'),
     Card(rank='7', suit='hearts'),
     Card(rank='5', suit='spades'),
     Card(rank='7', suit='clubs')]



The signature of the \__setitem__ special method is defined in The Python Language Reference in “3.3.6. Emulating container types”. Here we named the arguments deck, position, card—and not self, key, value as in the language reference—to show that every Python method starts life as a plain function, and naming the first argument self is merely a convention. This is OK in a console session, but in a Python source file it’s much better to use self, key, and value as documented.

The trick is that set_card knows that the deck object has an attribute named _cards, and _cards must be a mutable sequence. The set_card function is then attached to the FrenchDeck class as the \__setitem__ special method. This is an example of monkey patching: changing a class or module at runtime, without touching the source code. Monkey patching is powerful, but the code that does the actual patching is very tightly coupled with the program to be patched, often handling private and undocumented parts.

Besides being an example of monkey patching, Example 11-6 highlights that protocols are dynamic: random.shuffle doesn’t care what type of argument it gets, it only needs the object to implement part of the mutable sequence protocol. It doesn’t even matter if the object was “born” with the necessary methods or if they were somehow acquired later.

The theme of this chapter so far has been “duck typing”: operating with objects regardless of their types, as long as they implement certain protocols.

## Subclassing an ABC
Following Martelli’s advice, we’ll leverage an existing ABC, collections.MutableSe quence, before daring to invent our own. In Example 11-8, FrenchDeck2 is explicitly declared a subclass of collections.MutableSequence.


```python
# Exmaple 11-8: a subclass of collections.MutableSequence
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
    
    # need to enable shuffling
    def __setitem__(self, position, value):
        self._cards[position] = value
    
    # subclassing MutableSequence forces us to implement __delitem__,
    # an abstract method of that ABC.
    def __delitem__(self, position):
        del self._cards[position]
    
    # also required to implement insert, the third abstract method of MutableSequence.
    def insert(self, position, value):
        self._cards.insert(position, value)
```

Python does not check for the implementation of the abstract methods at import time (when the frenchdeck2.py module is loaded and compiled), but only at runtime when we actually try to instantiate FrenchDeck2. Then, if we fail to implement any abstract method, we get a TypeError exception with a message such as "Can't instantiate abstract class FrenchDeck2 with abstract methods \__delitem__, insert". That’s why we must implement \__delitem__ and insert, even if our FrenchDeck2 examples do not need those behaviors: the MutableSequence ABC demands them.

From Sequence, FrenchDeck2 inherits the following ready-to-use concrete methods: \__contains__, \__iter__, \__reversed__, index, and count. From MutableSequence, it gets append, reverse, extend, pop, remove, and \__iadd__.

The concrete methods in each collections.abc ABC are implemented in terms of the public interface of the class, so they work without any knowledge of the internal struc‐ ture of instances.


## ABCs in the Standard Library
Since Python 2.6, ABCs are available in the standard library. Most are defined in the collections.abc module, but there are others. You can find ABCs in the numbers and io packages, for example. But the most widely used is collections.abc. Let’s see what is available there.

### ABCs in collections.abc
* Iterable, Container, and Sized

Every collection should either inherit from these ABCs or at least implement com‐ patible protocols. Iterable supports iteration with __iter__, Container supports the in operator with __contains__, and Sized supports len() with __len__.

* Sequence, Mapping, and Set

These are the main immutable collection types, and each has a mutable subclass. A detailed diagram for MutableSequence is in Figure 11-2; for MutableMapping and MutableSet, there are diagrams in Chapter 3 (Figures 3-1 and 3-2).

* MappingView

In Python 3, the objects returned from the mapping methods .items(), .keys(), and .values() inherit from ItemsView, ValuesView, and ValuesView, respectively. The first two also inherit the rich interface of Set, with all the operators we saw in “Set Operations” on page 82.

* Callable and Hashable

These ABCs are not so closely related to collections, but collections.abc was the first package to define ABCs in the standard library, and these two were deemed important enough to be included. I’ve never seen subclasses of either Callable or Hashable. Their main use is to support the insinstance built-in as a safe way of determining whether an object is callable or hashable.

* Iterator

Note that iterator subclasses Iterable. We discuss this further in Chapter 14.



### The Numbers Tower of ABCs
The numbers package defines the so-called “numerical tower” (i.e., this linear hierarchy of ABCs), where Number is the topmost superclass, Complex is its immediate subclass, and so on, down to Integral:
* Number
* Complex
* Real
* Rational
* Integral

So if you need to check for an integer, use isinstance(x, numbers.Integral) to accept int, bool (which subclasses int) or other integer types that may be provided by external libraries that register their types with the numbers ABCs. And to satisfy your check, you or the users of your API may always register any compatible type as a virtual subclass of numbers.Integral.

If, on the other hand, a value can be a floating-point type, you write isinstance(x, numbers.Real), and your code will happily take bool, int, float, fractions.Frac tion, or any other noncomplex numerical type provided by an external library, such as NumPy, which is suitably registered.

## Defining and Using an ABC


```python
# Example 11-9: tombola is an ABC with two abstract methods and two concrete methods
import abc

class Tombola(abc.ABC):
    
    # An abstract method is marked with the @abstractmethod decorator,
    # and often its body is empty except for a docstring.
    @abc.abstractmethod
    def load(self, iterable):
        """Add items from an iterable"""
    
    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it, should raise LookupError when instance is empty"""
        
    def loaded(self):
        """Return 'True' if there's at least 1 item, 'False' otherwise"""
        return bool(self.inspect())
    
    def inspect(self):
        """Return a sorted tuple with the items currently inside"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))
```

The .inspect() method in Example 11-9 is perhaps a silly example, but it shows that, given .pick() and .load(...) we can inspect what’s inside the Tombola by picking all items and loading them back. The point of this example is to highlight that it’s OK to provide concrete methods in ABCs, as long as they only depend on other methods in the interface. Being aware of their internal data structures, concrete subclasses of Tombola may always override .inspect() with a smarter implementation, but they don’t have to.

The .loaded() method in Example 11-9 may not be as silly, but it’s expensive: it calls .inspect() to build the sorted tuple just to apply bool() on it. This works, but a concrete subclass can do much better, as we’ll see.

Note that our roundabout implementation of .inspect() requires that we catch a LookupError thrown by self.pick(). The fact that self.pick() may raise LookupEr ror is also part of its interface, but there is no way to declare this in Python, except in the documentation (see the docstring for the abstract pick method in Example 11-9.)

I chose the LookupError exception because of its place in the Python hierarchy of ex‐ ceptions in relation to IndexError and KeyError, the most likely exceptions to be raised by the data structures used to implement a concrete Tombola. Therefore, implementa‐ tions can raise LookupError, IndexError, or KeyError to comply. See Example 11-10 (for a complete tree, see “5.4. Exception hierarchy” of The Python Standard Library).


```python
# Example 11-11: A fake Tombola doesn't go undected
class Fake(Tombola):
    def pick(self):
        return 13
```


```python
# The class was created, no errors so far.
Fake
```




    __main__.Fake




```python
# TypeError is raised when we try to instantiate Fake.
# The message is very clear: Fake is considered abstract because it failed to implement load,
# one of the abstract methods declared in the Tombola ABC.
f = Fake()
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-21-a646eb69a2f6> in <module>()
    ----> 1 f = Fake()
    

    TypeError: Can't instantiate abstract class Fake with abstract methods load


### ABC Syntax Details

### Subclassing the Tombola ABC
Given the Tombola ABC, we’ll now develop two concrete subclasses that satisfy its in‐ terface. These classes were pictured in Figure 11-4, along with the virtual subclass to be discussed in the next section.

The BingoCage class in Example 11-12 is a variation of Example 5-8 using a better randomizer. This BingoCage implements the required abstract methods load and pick, inherits loaded from Tombola, overrides inspect, and adds \__call__.


```python
# Example 11-12: BingoCage is a concrete subclass of Tombola
import random

class BingoCage(Tombola):
    
    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)
    
    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)
        
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    
    def __call__(self):
        self.pick()
```


```python
# Example 11-13: LotteryBlower is a concrete subclass that override the inspect and loaded methods from Tombola
import random

class LotteryBlower(Tombola):
    
    def __init__(self, iterable):
        self._balls = list(iterable)
        
    def load(self, iterable):
        self._balls.extend(iterable)
        
    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotteryBlower')
        return self._balls.pop(position)
    
    def loaded(self):
        return bool(self._balls)
    
    def inspect(self):
        return tuple(sorted(self._balls))
```

### A Virtual Subclass of Tombola
An essential characteristic of goose typing—and the reason why it deserves a waterfowl name—is the ability to register a class as a virtual subclass of an ABC, even if it does not inherit from it. When doing so, we promise that the class faithfully implements the interface defined in the ABC—and Python will believe us without checking. If we lie, we’ll be caught by the usual runtime exceptions.

This is done by calling a register method on the ABC. The registered class then be‐ comes a virtual subclass of the ABC, and will be recognized as such by functions like issubclass and isinstance, but it will not inherit any methods or attributes from the ABC.


```python
# Example 11-14: class Tombolist is a virtual subclass of Tombola
from random import randrange

# Tombolist is registered as a virtual subclass of Tombola.
# Tombolist extends list.
@Tombola.register
class TomboList(list):
    
    def pick(self):
        # Tombolist inherits __bool__ from list, and that returns True if the list is not empty.
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')
    
    # Tombolist.load is the same as list.extend.
    load = list.extend
    
    def loaded(self):
        # loaded delegates to bool.
        return bool(self)
    
    def inspect(self):
        return tuple(sorted(self))
    
# If you’re using Python 3.3 or earlier,
# you can’t use .register as a class decorator. You must use standard call syntax.
# Tombola.register(TomboList)
```


```python
issubclass(TomboList, Tombola)
```




    True




```python
t = TomboList(range(100))
```


```python
isinstance(t, Tombola)
```




    True



However, inheritance is guided by a special class attribute named \__mro__—the Method Resolution Order. It basically lists the class and its superclasses in the order Python uses to search for methods.16 If you inspect the \__mro__ of TomboList, you’ll see that it lists only the “real” superclasses—list and object:


```python
TomboList.__mro__
```




    (__main__.TomboList, list, object)



Tombola is not in Tombolist.\__mro__, so Tombolist does not inherit any methods from Tombola.

## How the Tombola Subclasses Were Tested

## Usage of register in Practice
In Example 11-14, we used Tombola.register as a class decorator. Prior to Python 3.3, register could not be used like that—it had to be called as a plain function after the class definition, as suggested by the comment at the end of Example 11-14.

However, even if register can now be used as a decorator, it’s more widely deployed as a function to register classes defined elsewhere. For example, in the source code for the collections.abc module, the built-in types tuple, str, range, and memoryview are registered as virtual subclasses of Sequence like this:

```python
    Sequence.register(tuple)
    Sequence.register(str)
    Sequence.register(range)
    Sequence.register(memoryview)
```

Several other built-in types are registered to ABCs in _collections_abc.py. Those regis‐ trations happen only when that module is imported, which is OK because you’ll have to import it anyway to get the ABCs: you need access to MutableMapping to be able to write isinstance(my_dict, MutableMapping).
We’ll wrap up this chapter by explaining a bit of ABC magic that Alex Martelli performed in “Waterfowl and ABCs” on page 314.

## Geese Can Behave as Ducks


```python
from collections import abc
class Struggle:
    def __len__(self):
        return 23
```


```python
isinstance(Struggle(), abc.Sized)
```




    True




```python
issubclass(Struggle, abc.Sized)
```




    True



Class Struggle is considered a subclass of abc.Sized by the issubclass function (and, consequently, by isinstance as well) because abc.Sized implements a special class method named \__subclasshook__. See Example 11-17.

```python
# Example 11-17: Sized definition from the source code of Lib/_collections_abc.py
class Sized(metaclass=ABCMeta):
    
    __slots__ = ()
    
    @abstractmethod
    def __len__(self):
        return 0
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Sized:
            # If there is an attribute named __len__ in the __dict__ of 
            # any class listed inC.__mro__ (i.e., C and its superclasses)...
            if any('__len__' in B.__dict__ for B in C.__mro__):
                # ...return True, signaling that C is a virtual subclass of Sized.
                return True
        # Otherwise return NotImplemented to let the subclass check proceed.
        return NotImplemented
```
