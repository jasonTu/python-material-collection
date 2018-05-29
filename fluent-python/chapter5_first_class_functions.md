
## Treating a Function Like an Object


```python
# Example 5-1: Create and test a function then read its __doc__ and check its type
def factorial(n):
    '''Return n!'''
    return 1 if n < 2 else n * factorial(n-1)
```


```python
factorial(4)
```




    24




```python
factorial.__doc__
```




    'Return n!'




```python
type(factorial)
```




    function




```python
# Example 5-2: Use function through a different name, and pass function as argument
fact = factorial
fact
```




    <function __main__.factorial>




```python
fact(5)
```




    120




```python
map(factorial, range(10))
```




    <map at 0x7fe23c67d710>




```python
list(map(factorial, range(6)))
```




    [1, 1, 2, 6, 24, 120]



## Higher-Ordered Functions


```python
# Example 5-3: Sorting a list of words by length
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'respberry', 'banana']
sorted(fruits, key=len)
```




    ['fig', 'apple', 'cherry', 'banana', 'respberry', 'strawberry']




```python
# Example 5-4: Sorting a list of words by their reversed spelling
def reverse(word):
    return word[::-1]
reverse('testing')
```




    'gnitset'




```python
sorted(fruits, key=reverse)
```




    ['banana', 'apple', 'fig', 'respberry', 'strawberry', 'cherry']



## Modern Replacements for map, filter and reduce
Functional languages commonly offer the map, filter, and reduce higher-order func‐
tions (sometimes with different names). The map and filter functions are still builtins in Python 3, but since the introduction of list comprehensions and generator ex‐
pressions, they are not as important. A listcomp or a genexp does the job of map and
filter combined, but is more readable.


```python
# Example 5-5
list(map(fact, range(6)))
```




    [1, 1, 2, 6, 24, 120]




```python
[fact(n) for n in range(6)]
```




    [1, 1, 2, 6, 24, 120]




```python
list(map(factorial, filter(lambda n: n % 2, range(6))))
```




    [1, 6, 120]




```python
[factorial(n) for n in range(6) if n % 2]
```




    [1, 6, 120]




```python
# Example 5-6
from functools import reduce
from operator import add

reduce(add, range(6))
```




    15




```python
sum(range(6))
```




    15



## Anonymous Functions
The best use of anonymous functions is in the context of an argument list. 


```python
# Example 5-7
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'respberry', 'banana']
sorted(fruits, key=lambda word: word[::-1])
```




    ['banana', 'apple', 'fig', 'respberry', 'strawberry', 'cherry']



## User-Defined Callable Types


```python
# Example 5-8
import random

class BingoCage:
    
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)
    
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    
    def __call__(self):
        return self.pick()
```


```python
bingo = BingoCage(range(3))
bingo.pick()
```




    2




```python
bingo()
```




    1




```python
callable(bingo)
```




    True



## From Positional to Keyword-Only Parameters
One of the best features of Python functions is the extremely flexible parameter handling
mechanism, enhanced with keyword-only arguments in Python 3. Closely related are
the use of * and ** to “explode” iterables and mappings into separate arguments when
we call a function. To see these features in action, see the code for Example 5-10 and
tests showing its use in Example 5-11.


```python
# Example 5-10
def tag(name, *content, cls=None, **attrs):
    '''Generate one or more HTML tags'''
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        print(attrs)
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
        print(attr_str)
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s<%s/' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)
```


```python
tag('br')
```




    '<br />'




```python
tag('p', 'hello')
```




    '<p>hello<p/'




```python
print(tag('p', 'hello', 'world'))
```

    <p>hello<p/
    <p>world<p/



```python
tag('p', 'hello', id=33)
```

     id="33"





    '<p id="33">hello<p/'




```python
print(tag('p', 'hello', 'world', cls='sidebar'))
```

     class="sidebar"
    <p class="sidebar">hello<p/
    <p class="sidebar">world<p/



```python
# Even the first positional argument can be passed as a keyword when tag is called
tag(content='testing', name="img")
```

    {'content': 'testing'}
     content="testing"





    '<img content="testing" />'




```python
# Prefixing the my_tag dict with ** passes all its items as separate arguments, 
# which are then bound to the named parameters, with the remaining caught by **attrs.
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
tag(**my_tag)
```

    {'class': 'framed', 'src': 'sunset.jpg', 'title': 'Sunset Boulevard'}
     class="framed" src="sunset.jpg" title="Sunset Boulevard"





    '<img class="framed" src="sunset.jpg" title="Sunset Boulevard" />'




```python
tag(my_tag)
```




    "<{'cls': 'framed', 'src': 'sunset.jpg', 'title': 'Sunset Boulevard', 'name': 'img'} />"



## Retrieving Information About Parameters
Within a function object, the \__defaults__ attribute holds a tuple with the default
values of positional and keyword arguments. The defaults for keyword-only arguments
appear in \__kwdefaults__. The names of the arguments, however, are found within the
\__code__ attribute, which is a reference to a code object with many attributes of its own


```python
# Example 5-15: Function to shorten a string by clipping at a space near the desired length
def clip(text, max_len=80):
    '''Return text clipped at the last space before or after max_len'''
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()
```


```python
# Shos the values of __defaults__, __oode__.co_varnames and __code__.co_argcount
clip.__defaults__
```




    (80,)




```python
clip.__code__
```




    <code object clip at 0x104892420, file "<ipython-input-1-627911fb9fde>", line 2>




```python
clip.__code__.co_varnames
```




    ('text', 'max_len', 'end', 'space_before', 'space_after')




```python
clip.__code__.co_argcount
```




    2




```python
# Example 5-17: Extracting the function signature
from inspect import signature
sig = signature(clip)
sig
```




    <Signature (text, max_len=80)>




```python
str(sig)
```




    '(text, max_len=80)'




```python
for name, param in sig.parameters.items():
    print(param.kind, ':', name, '=', param.default)
```

    POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'>
    POSITIONAL_OR_KEYWORD : max_len = 80



```python
# Example 5-18: Binding the function signature from the tag function in Example 5-10 to a dict of arguments
import inspect
sig = inspect.signature(tag)
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
bound_args = sig.bind(**my_tag)
bound_args
```




    <BoundArguments (name='img', cls='framed', attrs={'title': 'Sunset Boulevard', 'src': 'sunset.jpg'})>




```python
for name, value in bound_args.arguments.items():
    print(name, '=', value)
```

    name = img
    cls = framed
    attrs = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}



```python
del my_tag['name']
```


```python
# This can be used by a framework to validate arguments prior to the actual function invocation.
bound_args = sig.bind(**my_tag)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-18-745c0e30e124> in <module>()
          1 # This can be used by a framework to validate arguments prior to the actual function invocation.
    ----> 2 bound_args = sig.bind(**my_tag)
    

    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/inspect.py in bind(*args, **kwargs)
       2967         if the passed arguments can not be bound.
       2968         """
    -> 2969         return args[0]._bind(args[1:], kwargs)
       2970 
       2971     def bind_partial(*args, **kwargs):


    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/inspect.py in _bind(self, args, kwargs, partial)
       2882                             msg = 'missing a required argument: {arg!r}'
       2883                             msg = msg.format(arg=param.name)
    -> 2884                             raise TypeError(msg) from None
       2885             else:
       2886                 # We have a positional argument to process


    TypeError: missing a required argument: 'name'


## Function Annotations(注释)


```python
# Example 5-19: Annotated clip function
def clip(text:str, max_len:'int > 0'=80) -> str:
    """Return text clipped at the last space before or after max_len"""
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()
```


```python
# The only thing Python does with annotations is to store them in the __annotations__ attribute of the function. 
# Nothing else: no checks, enforcement, validation, or any other action is performed.
clip.__annotations__
```




    {'text': str, 'max_len': 'int > 0', 'return': str}




```python
from inspect import signature
sig = signature(clip)
sig.return_annotation
```




    str




```python
for param in sig.parameters.values():
    note = repr(param.annotation).ljust(13)
    print(note, ':', param.name.ljust(15), '=', param.default)
```

    <class 'str'> : text            = <class 'inspect._empty'>
    'int > 0'     : max_len         = 80


## Packages for Functional Programming

### The operator Module


```python
# Example 5-21: Factorial implemented with reduce and an anonymous function.
from functools import reduce
def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))
```


```python
# Example 5-22: Factorial implemented with reduce and operator.mul
from functools import reduce
from operator import mul
def fact2(n):
    return reduce(mul, range(1, n+1))
```


```python
fact(5)
```




    120




```python
fact2(5)
```




    120




```python
# Example 5-23: Demo of itemgetter to sort a list of tuples.
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
```


```python
from operator import itemgetter
for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
```

    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386))



```python
# Because itemgetter uses the [] operator, it supports not only sequences but also mappings and class that implements __getitem__.
cc_name = itemgetter(1, 0)
for city in metro_data:
    print(cc_name(city))
```

    ('JP', 'Tokyo')
    ('IN', 'Delhi NCR')
    ('MX', 'Mexico City')
    ('US', 'New York-Newark')
    ('BR', 'Sao Paulo')



```python
# Example 5-24: Demo of attrgetter to process a previously defined list of namedtuple called metro_data
from collections import namedtuple
LatLong = namedtuple('LatLong', 'lat long')
Metropolis = namedtuple('Metropolis', 'name cc pop coord')
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) 
               for name, cc, pop, (lat, long) in metro_data]
metro_areas
```




    [Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667)),
     Metropolis(name='Delhi NCR', cc='IN', pop=21.935, coord=LatLong(lat=28.613889, long=77.208889)),
     Metropolis(name='Mexico City', cc='MX', pop=20.142, coord=LatLong(lat=19.433333, long=-99.133333)),
     Metropolis(name='New York-Newark', cc='US', pop=20.104, coord=LatLong(lat=40.808611, long=-74.020386)),
     Metropolis(name='Sao Paulo', cc='BR', pop=19.649, coord=LatLong(lat=-23.547778, long=-46.635833))]




```python
metro_areas[0].coord.lat
```




    35.689722




```python
from operator import attrgetter
name_lat = attrgetter('name', 'coord.lat')
for city in sorted(metro_areas, key=attrgetter('coord.lat')):
    print(name_lat(city))
```

    ('Sao Paulo', -23.547778)
    ('Mexico City', 19.433333)
    ('Delhi NCR', 28.613889)
    ('Tokyo', 35.689722)
    ('New York-Newark', 40.808611)



```python
# Example 5-25: Demo of methodcaller. second test shows the binding of extra arguments
from operator import methodcaller
s = 'The time has come'
upcase = methodcaller('upper')
upcase(s)
```




    'THE TIME HAS COME'




```python
hiphenate = methodcaller('replace', ' ', '-')
hiphenate(s)
```




    'The-time-has-come'



### Freezing Arguments with functools.partial


```python
# Example 5-26: Using partial to use a two-argument function where a one-argument callable is required
from operator import mul
from functools import partial
triple = partial(mul, 3)
triple(7)
```




    21




```python
list(map(triple, range(1, 10)))
```




    [3, 6, 9, 12, 15, 18, 21, 24, 27]




```python
# Example 5-27: Building a convenient Unicode normalizing function with partial
import unicodedata, functools
nfc = functools.partial(unicodedata.normalize, 'NFC')
s1 = 'café'
s2 = 'cafe\u0301'
s1, s2
```




    ('café', 'café')




```python
s1 == s2
```




    False




```python
nfc(s1) == nfc(s2)
```




    True




```python
nfc.func
```




    <function unicodedata.normalize(form, unistr, /)>




```python
nfc.args
```




    ('NFC',)




```python
nfc.keywords
```




    {}


