
## Sentence Take #1: A Sequence of Words


```python
# Example 14-1: shows a Sentence class that extracts words from a text by index
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
        
    def __getitem__(self, index):
        return self.words[index]
    
    def __len__(self):
        return len(self.words)
    
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
```


```python
# Example 14-2: Testing iteration on a Sentence instance
s = Sentence('"The time has come," the Walrus said.')
```


```python
s
```




    Sentence('"The time ha... Walrus said.')




```python
for word in s:
    print(word)
```

    The
    time
    has
    come
    the
    Walrus
    said



```python
# Being iterable, Sentence objects can be used as input to build lists and other iterable types.
list(s)
```




    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']




```python
s[0]
```




    'The'



### Why Sequences Are Iterable: The iter Function
Whenever the interpreter needs to iterate over an object x, it automatically calls iter(x). The iter built-in function:
1. Checks whether the object implements \__iter__, and calls that to obtain an iterator.
2. If \__iter__ is not implemented, but \__getitem__ is implemented, Python creates
an iterator that attempts to fetch items in order, starting from index 0 (zero).
3. If that fails, Python raises TypeError, usually saying “C object is not iterable,” where
C is the class of the target object.

That is why any Python sequence is iterable: they all implement \__getitem__. In fact, the standard sequences also implement \__iter__, and yours should too, because the special handling of \__getitem__ exists for backward compatibility reasons and may be gone in the future (although it is not deprecated as I write this).

As mentioned in “Python Digs Sequences” on page 310, this is an extreme form of duck typing: an object is considered iterable not only when it implements the special method \__iter__, but also when it implements \__getitem__, as long as \__getitem__ accepts int keys starting from 0.

In the goose-typing approach, the definition for an iterable is simpler but not as flexible: an object is considered iterable if it implements the \__iter__ method. No subclassing or registration is required, because abc.Iterable implements the \__subclasshook__, as seen in “Geese Can Behave as Ducks” on page 338. Here is a demonstration:


```python
class Foo:
    def __iter__(self):
        pass
```


```python
from collections import abc
```


```python
issubclass(Foo, abc.Iterable)
```




    True




```python
isinstance(Foo(), abc.Iterable)
```




    True



Explicitly checking whether an object is iterable may not be worthwhile if right after the check you are going to iterate over the object. After all, when the iteration is attempted on a noniterable, the exception Python raises is clear enough: TypeError: 'C' object is not iterable . If you can do better than just raising TypeError, then do so in a try/except block instead of doing an explicit check. The explicit check may make sense if you are holding on to the object to iterate over it later; in this case, catching the error early may be useful.

## Iterables Versus Iterators
From the explanation in “Why Sequences Are Iterable: The iter Function” on page 404 we can extrapolate a definition:
* iterable

Any object from which the iter built-in function can obtain an iterator. Objects implementing an \__iter__ method returning an iterator are iterable. Sequences Iterables Versus Iterators are always iterable; as are objects implementing a \__getitem__ method that takes 0-based indexes.

It’s important to be clear about the relationship between iterables and iterators: Python obtains iterators from iterables.

Here is a simpleforloop iterating over astr. Thestr'ABC'is the iterable here. You don’t see it, but there is an iterator behind the curtain:


```python
s ='ABC'
for char in s:
    print(char)
```

    A
    B
    C


If there was no for statement and we had to emulate the for machinery by hand with a while loop, this is what we’d have to write:


```python
s = 'ABC'
it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        del it
        break
```

    A
    B
    C


StopIteration signals that the iterator is exhausted. This exception is handled inter‐ nally in for loops and other iteration contexts like list comprehensions, tuple unpacking, etc.

The standard interface for an iterator has two methods:
* \__next__

Returns the next available item, raising StopIteration when there are no more items.

* \__iter__

Returns self; this allows iterators to be used where an iterable is expected, for example, in a for loop.

The Iterator ABC implements __iter__ by doing return self. This allows an iterator to be used wherever an iterable is required. The source code for abc.Iterator is in Example 14-3.

```python
# Example 14-3. abc.Iterator class; extracted from Lib/_collections_abc.py 
class Iterator(Iterable):
    __slots__ = ()
    
    @abstractmethod
    def __next__(self):
        'Return the next item from the iterator. When exhausted, raise StopIteration'
        raise StopIteration
        
    def __iter__(self):
        return self
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Iterator:
            if (any("__next__" in B.__dict__ for B in C.__mro__) and
                any("__iter__" in B.__dict__ for B in C.__mro__)):
                    return True
        return NotImplemented
```

Back to our Sentence class from Example 14-1, you can clearly see how the iterator is built by iter(...) and consumed by next(...) using the Python console:


```python
s3 = Sentence('Pig and Pipper')
it = iter(s3)
it
```




    <iterator at 0x1109a2160>




```python
next(it)
```




    'Pig'




```python
next(it)
```




    'and'




```python
next(it)
```




    'Pipper'




```python
next(it)
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    <ipython-input-22-bc1ab118995a> in <module>()
    ----> 1 next(it)
    

    StopIteration: 



```python
# Once exhausted, an iterator becomes useless.
list(it)
```




    []




```python
# To go over the sentence again, a new iterator must be built.
list(iter(s3))
```




    ['Pig', 'and', 'Pipper']



Because the only methods required of an iterator are \__next__ and \__iter__, there is no way to check whether there are remaining items, other than to call next() and catch StopInteration. Also, it’s not possible to “reset” an iterator. If you need to start over, you need to call iter(...) on the iterable that built the iterator in the first place. Calling iter(...) on the iterator itself won’t help, because—as mentioned—Itera tor.\__iter__ is implemented by returning self, so this will not reset a depleted iter‐ ator.

To wrap up this section, here is a definition for iterator:
* iterator

Any object that implements the \__next__ no-argument method that returns the next item in a series or raises StopIteration when there are no more items. Python iterators also implement the \__iter__ method so they are iterable as well.

## Sentence Take #2: A Classic Iterator
The next Sentence class is built according to the classic Iterator design pattern following the blueprint in the GoF book. Note that this is not idiomatic Python, as the next re‐ factorings will make very clear. But it serves to make explicit the relationship between the iterable collection and the iterator object.


```python
# Example 14-4: Sentence implemented using the Iterator patern
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    
    def __repr__(self):
        return 'Setence(%)' % reprlib.repr(self.text)
    
    def __iter__(self):
        return SetenceIterator(self.words)


class SentenceIterator:
    
    def __init__(self, words):
        self.words = words
        self.index = 0
    
    def __next_(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word
    
    def __iter__(self):
        return self
```

Note that implementing \__iter__ in SentenceIterator is not actually needed for this example to work, but the it’s the right thing to do: iterators are supposed to implement both \__next__ and \__iter__, and doing so makes our iterator pass the issubclass(Sen tenceInterator, abc.Iterator) test. If we had subclassed SentenceIterator from abc.Iterator, we’d inherit the concrete abc.Iterator.\__iter__ method.

That is a lot of work (for us lazy Python programmers, anyway). Note how most code in SentenceIterator deals with managing the internal state of the iterator. Soon we’ll see how to make it shorter. But first, a brief detour to address an implementation shortcut that may be tempting, but is just wrong.

### Making Sentence an Iterator: Bad Idea
A common cause of errors in building iterables and iterators is to confuse the two. To be clear: iterables have an \__iter__ method that instantiates a new iterator every time. Iterators implement a \__next__ method that returns individual items, and an \__iter__ method that returns self.

Therefore, iterators are also iterable, but iterables are not iterators.

It may be tempting to implement \__next__ in addition to \__iter__ in the Sentence class, making each Sentence instance at the same time an iterable and iterator over itself. But this is a terrible idea. It’s also a common anti-pattern, according to Alex Mar‐ telli who has a lot of experience with Python code reviews.

The “Applicability” section4 of the Iterator design pattern in the GoF book says: Use the Iterator pattern
* to access an aggregate object’s contents without exposing its internal representation.
* to support multiple traversals of aggregate objects.
* to provide a uniform interface for traversing different aggregate structures (that is, to support polymorphic iteration).

To “support multiple traversals” it must be possible to obtain multiple independent iterators from the same iterable instance, and each iterator must keep its own internal state, so a proper implementation of the pattern requires each call to iter(my_itera ble) to create a new, independent, iterator. That is why we need the SentenceItera tor class in this example.

## Setence Take #3: A Generator Function
A Pythonic implementation of the same functionality uses a generator function to re‐ place the SequenceIterator class. A proper explanation of the generator function comes right after Example 14-5.


```python
# Example 14-5: Sentence implemented using a generator function
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    
    def __repr__(self):
        return 'Setence(%)' % reprlib.repr(self.text)
    
    def __iter__(self):
        for word in self.words:
            yield word
        # This return is not needed; the function can just “fall-through” and return automatically.
        # Either way, a generator function doesn’t raise StopIteration:
        # it simply exits when it’s done producing values.
        return
```

Back in the Sentence code in Example 14-4, \__iter__ called the SentenceIterator constructor to build an iterator and return it. Now the iterator in Example 14-5 is in fact a generator object, built automatically when the \__iter__ method is called, because \__iter__ here is a generator function.

### How a Generator Function Works
Any Python function that has the yield keyword in its body is a generator function: a function which, when called, returns a generator object. In other words, a generator function is a generator factory.


```python
def gen_123():
    yield 1
    yield 2
    yield 3
```


```python
gen_123
```




    <function __main__.gen_123()>




```python
gen_123()
```




    <generator object gen_123 at 0x110974990>




```python
# When the generator function body runs to the end, the generator object raises StopIteration. 
# The for loop machinery catches that exception, and the loop terminates cleanly.
for i in gen_123():
    print(i)
```

    1
    2
    3



```python
g = gen_123()
```


```python
next(g)
```




    1




```python
next(g)
```




    2




```python
next(g)
```




    3




```python
next(g)
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    <ipython-input-38-e734f8aca5ac> in <module>()
    ----> 1 next(g)
    

    StopIteration: 


Now hopefully it’s clear how Sentence.\__iter__ in Example 14-5 works: \__iter__ is a generator function which, when called, builds a generator object that implements the iterator interface, so the SentenceIterator class is no longer needed.

This second version of Sentence is much shorter than the first, but it’s not as lazy as it could be. Nowadays, laziness is considered a good trait, at least in programming languages and APIs. A lazy implementation postpones producing values to the last possible moment. This saves memory and may avoid useless processing as well.

## Setence Take #4: A Lazy Implementation


```python
# Example 14-7: Sentence implemented using a generator function calling the re.finditer generator function
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    
    def __init__(self, text):
        self.text = text
        
    def __repr__(self):
        return 'Setence(%)' % reprlib.repr(self.text)
    
    def __iter__(self):
        # finditer builds an iterator over the matches of RE_WORD on self.text,
        # yielding MatchObject instances.
        for match in RE_WORD.finditer(self.text):
            # match.group() extracts the actual matched text from the MatchObject instance.
            yield match.group()
```

## Sentence Take #5: A Generator Expression
Simple generator functions like the one in the previous Sentence class (Example 14-7) can be replaced by a generator expression.

A generator expression can be understood as a lazy version of a list comprehension: it does not eagerly build a list, but returns a generator that will lazily produce the items on demand. In other words, if a list comprehension is a factory of lists, a generator expression is a factory of generators.


```python
# Example 14-8: The gen_AB generator function is used by a list comprehension, then by a generator expression
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end')
```


```python
# The list comprehension eagerly iterates over the items 
# yielded by the generator object produced by calling gen_AB(): 'A' and 'B'.
# Note the output in the next lines: start, continue, end.
res1 = [x*3 for x in gen_AB()]
```

    start
    continue
    end



```python
# This for loop is iterating over the res1 list produced by the list comprehension.
for i in res1:
    print('-->', i)
```

    --> AAA
    --> BBB



```python
# The generator expression returns res2. The call to gen_AB() is made,
# but that call returns a generator, which is not consumed here.
res2 = (x*3 for x in gen_AB())
```


```python
res2
```




    <generator object <genexpr> at 0x1109b71a8>




```python
for i in res2:
    print(i)
```

    start
    AAA
    continue
    BBB
    end



```python
for i in gen_AB():
    print(i)
```

    start
    A
    continue
    B
    end


So, a generator expression produces a generator, and we can use it to further reduce the code in the Sentence class. See Example 14-9.


```python
# Example 14-9: Sentence implemented using a generator expression
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    
    def __init__(self, text):
        self.text = text
    
    def __repr__(self):
        return 'Setence(%)' % reprlib.repr(self.text)
    
    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))
```

The only difference from Example 14-7 is the \__iter__ method, which here is not a generator function (it has no yield) but uses a generator expression to build a generator and then returns it. The end result is the same: the caller of \__iter__ gets a generator object.

Generator expressions are syntactic sugar: they can always be replaced by generator functions, but sometimes are more convenient. The next section is about generator expression usage.

## Generator Expressions: WHen to Use Them
For the simpler cases, a generator expression will do, and it’s easier to read at a glance, as the Vector example shows.

My rule of thumb in choosing the syntax to use is simple: if the generator expression spans more than a couple of lines, I prefer to code a generator function for the sake of readability. Also, because generator functions have a name, they can be reused. You can always name a generator expression and use it later by assigning it to a variable, of course, but that is stretching its intended usage as a one-off generator.

## Another Example: Arithmetic Progression Generator
The classic Iterator pattern is all about traversal: navigating some data structure. But a standard interface based on a method to fetch the next item in a series is also useful when the items are produced on the fly, instead of retrieved from a collection. For example, the range built-in generates a bounded arithmetic progression (AP) of inte‐ gers, and the itertools.count function generates a boundless AP.

We’ll cover itertools.count in the next section, but what if you need to generate a bounded AP of numbers of any type?


```python
# Example 14-11: The ArithmeticProgression class
class ArithmeticProgression:
    
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end
    
    def __iter__(self):
        result = type(self.begin + self.step)(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index
```


```python
# Example 14-10
ap = ArithmeticProgression(0,1 , 3)
list(ap)
```




    [0, 1, 2]




```python
apc = ArithmeticProgression
```


```python
ap = apc(1, .5, 3)
list(ap)
```




    [1.0, 1.5, 2.0, 2.5]




```python
ap = apc(0, 1/3, 1)
list(ap)
```




    [0.0, 0.3333333333333333, 0.6666666666666666]




```python
from fractions import Fraction
```


```python
ap = apc(0, Fraction(1, 3), 1)
list(ap)
```




    [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]




```python
from decimal import Decimal
```


```python
ap = apc(0, Decimal('.1'), .3)
list(ap)
```




    [Decimal('0'), Decimal('0.1'), Decimal('0.2')]



The ArithmeticProgression class from Example 14-11 works as intended, and is a clear example of the use of a generator function to implement the \__iter__ special method. However, if the whole point of a class is to build a generator by implementing \__iter__, the class can be reduced to a generator function. A generator function is, after all, a generator factory.


```python
# Example 14-12: The aritprog_gen generator function
def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index
```

### Arithmetic Progession with itertools
The itertools module in Python 3.4 has 19 generator functions that can be combined in a variety of interesting ways.

For example, the itertools.count function returns a generator that produces numbers. Without arguments, it produces a series of integers starting with 0. But you can provide optional start and step values to achieve a result very similar to our aritprog_gen functions:


```python
import itertools
gen = itertools.count(1, .5)
```


```python
next(gen)
```




    1




```python
next(gen)
```




    1.5




```python
next(gen)
```




    2.0




```python
next(gen)
```




    2.5




```python
gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))
```


```python
list(gen)
```




    [1, 1.5, 2.0, 2.5]




```python
# Example 14-13: this works like the previous artiprog_gen function
import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
```

## Generator Functions in the Standard Library

## New Syntax in Python 3.3: yield from
yield from i replaces the inner for loop completely. The use of yield from in this example is correct, and the code reads better, but it seems like mere syntactic sugar. Besides replacing a loop, yield from creates a channel connecting the inner generator directly to the client of the outer generator. This channel becomes really im‐ portant when generators are used as coroutines and not only produce but also consume values from the client code. Chapter 16 dives into coroutines, and has several pages explaining why yield from is much more than syntactic sugar.


```python
def chain(*iterables):
    for it in iterables:
        for i in it:
            yield i
```


```python
s = 'abc'
t = tuple(range(3))
list(chain(s, t))
```




    ['a', 'b', 'c', 0, 1, 2]




```python
def chain(*iterables):
    for i in iterables:
        yield from i
```


```python
list(chain(s, t))
```




    ['a', 'b', 'c', 0, 1, 2]



## Iterable Reducing Functions

## A Closer Look at the iter Function
As we’ve seen, Python calls iter(x) when it needs to iterate over an object x.

But iter has another trick: it can be called with two arguments to create an iterator from a regular function or any callable object. In this usage, the first argument must be a callable to be invoked repeatedly (with no arguments) to yield values, and the second argument is a sentinel: a marker value which, when returned by the callable, causes the iterator to raise StopIteration instead of yielding the sentinel.


```python
from random import randint
def d6():
    return randint(1, 6)
```


```python
d6_iter = iter(d6, 1)
d6_iter
```




    <callable_iterator at 0x1109da6a0>




```python
for roll in d6_iter:
    print(roll)
```

    4
    2
    3


Note that the iter function here returns a callable_iterator. The for loop in the example may run for a very long time, but it will never display 1, because that is the sentinel value. As usual with iterators, the d6_iter object in the example becomes use‐ less once exhausted. To start over, you must rebuild the iterator by invoking iter(...) again.

A useful example is found in the iter built-in function documentation. This snippet reads lines from a file until a blank line is found or the end of file is reached:

```python
with open('mydata.txt') as fp:
    for line in iter(fp.readline, ''):
        process_line(line)
```

## Generator as Coroutines
About five years after generator functions with the yield keyword were introduced in Python 2.2, PEP 342 — Coroutines via Enhanced Generators was implemented in Python 2.5. This proposal added extra methods and functionality to generator objects, most notably the .send() method.

Like .\__next__(), .send() causes the generator to advance to the next yield, but it also allows the client using the generator to send data into it: whatever argument is passed to .send() becomes the value of the corresponding yield expression inside the generator function body. In other words, .send() allows two-way data exchange be‐ tween the client code and the generator—in contrast with .\__next__(), which only lets the client receive data from the generator.

This is such a major “enhancement” that it actually changes the nature of generators: when used in this way, they become coroutines. David Beazley—probably the most pro‐ lific writer and speaker about coroutines in the Python community—warned in a fa‐ mous PyCon US 2009 tutorial:

* Generators produce data for iteration
* Coroutines are consumers of data
* To keep your brain from exploding, you don’t mix the two concepts together
* Coroutines are not related to iteration
* Note: There is a use of having yield produce a value in a coroutine, but it’s not tied to iteration.
