
## List Comprehensions and Generator Expressions

### List Comprehensions and Readability


```python
# Exmaple 2-1
symbols = '一个中国人'
codes = []
for symbol in symbols:
    codes.append(ord(symbol))
codes
```




    [19968, 20010, 20013, 22269, 20154]




```python
# Example 2-2
symbols = '一个中国人'
codes = [ord(symbol) for symbol in symbols]
codes
```




    [19968, 20010, 20013, 22269, 20154]



### Listcomps Versus map and filter


```python
# Example 2-3
symbols = '一个中国人'
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
beyond_ascii
```




    [19968, 20010, 20013, 22269, 20154]




```python
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
beyond_ascii
```




    [19968, 20010, 20013, 22269, 20154]



### Cartesian Product


```python
# Example 2-4
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
tshirts
```




    [('black', 'S'),
     ('black', 'M'),
     ('black', 'L'),
     ('white', 'S'),
     ('white', 'M'),
     ('white', 'L')]




```python
tshirts = [(color, size) for size in sizes for color in colors]
tshirts
```




    [('black', 'S'),
     ('white', 'S'),
     ('black', 'M'),
     ('white', 'M'),
     ('black', 'L'),
     ('white', 'L')]



### Generator Expressions


```python
## Example 2-5
symbols = '一个中国人'
# 如果生成器表达式作为函数的唯一参数，则无需添加外层的括号
tuple(ord(symbol) for symbol in symbols)
```




    (19968, 20010, 20013, 22269, 20154)




```python
import array
# 第二个参数是一个生成器
array.array('I', (ord(symbol) for symbol in symbols))
```




    array('I', [19968, 20010, 20013, 22269, 20154])




```python
# Example 2-6
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
    print(tshirt)
```

    black S
    black M
    black L
    white S
    white M
    white L


## Tuples are not just Immutable Lists

### Tuples as Records


```python
# Exmaple 2-7
lax_coordinates = (33.9425, -118.408056)
city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
for passport in sorted(traveler_ids):
    print('%s/%s' % passport)
```

    BRA/CE342567
    ESP/XDA205856
    USA/31195855



```python
# For循环知道如何分别对country和_赋值，这被称为unpacking
for country, _ in traveler_ids:
    print(country)
```

    USA
    BRA
    ESP


### Tuple unpacking


```python
lax_coordinates = (33.9425, -118.408056)
# Tuple unpacking
latitude, longitude = lax_coordinates
latitude
```




    33.9425




```python
# Tuple unpacking for swap
a = 1
b = 2
a, b = b, a
a
```




    2



### Using * to grab excess items


```python
# Parallel assignment
a, b, *rest = range(5)
a, b, rest
```




    (0, 1, [2, 3, 4])




```python
a, b, *rest = range(3)
a, b, rest
```




    (0, 1, [2])




```python
a, b, *rest = range(2)
a, b, rest
```




    (0, 1, [])




```python
a, *body, c, d = range(5)
a, body, c, d
```




    (0, [1, 2], 3, 4)




```python
*head, b, c, d = range(5)
head, b, c, d
```




    ([0, 1], 2, 3, 4)



### Nested Tuple Unpacking


```python
# Example 2-8
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 70.208889)),
]
print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
fmt = '{:15} | {:9.4f} | {:9.4f}'
# By assigning the last field to a tuple, we unpack the coordinates.
for name, cc, pop, (latitude, longitude) in metro_areas:
    if longitude > 100:
        print(fmt.format(name, latitude, longitude))
```

                    |   lat.    |   long.  
    Tokyo           |   35.6897 |  139.6917


### Named Tuples


```python
# Example 2-9
from collections import namedtuple
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
tokyo
```




    City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))




```python
tokyo.population
```




    36.933




```python
tokyo[2]
```




    36.933




```python
# Example 2-10
City._fields
```




    ('name', 'country', 'population', 'coordinates')




```python
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)
delhi._asdict()
```




    OrderedDict([('name', 'Delhi NCR'),
                 ('country', 'IN'),
                 ('population', 21.935),
                 ('coordinates', LatLong(lat=28.613889, long=77.208889))])




```python
delhi.coordinates
```




    LatLong(lat=28.613889, long=77.208889)



## Slicing

### Why Slices and Range Exclude the Last Item
* It works well with the zero-based indexing used in Python, C and other languages
* It’s easy to see the length of a slice or range when only the stop position is given: range(3) and my_list[:3] both produce three items
* It’s easy to compute the length of a slice or range when start and stop are given: just subtract stop - start
* It’s easy to split a sequence in two parts at any index x, without overlapping: simply get my_list[:x] and my_list[x:]. For example:

### Slice Object
seq[start:stop:step] --> seq.__get_item__(slice(start, stop, step))


```python
s = 'bicycle'
s[::3]
```




    'bye'




```python
s[::-1]
```




    'elcycib'




```python
s[::-2]
```




    'eccb'




```python
s[slice(0, 3, 1)]
```




    'bic'



### Assigning to Slices


```python
l = list(range(10))
l
```




    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]




```python
l[2:5] = [20, 30]
l
```




    [0, 1, 20, 30, 5, 6, 7, 8, 9]




```python
del l[5:7]
l
```




    [0, 1, 20, 30, 5, 8, 9]




```python
l[3::2] = [11, 22]
l
```




    [0, 1, 20, 11, 5, 22, 9]




```python
# When the target of the assigment is a slice, the right side must be an iterable objet
l[2:5] = 100
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-53-29071849310c> in <module>()
          1 # When the target of the assigment is a slice, the right side must be an iterable objet
    ----> 2 l[2:5] = 100
    

    TypeError: can only assign an iterable


## Using + and * with Sequences


```python
l = [1, 2, 3]
l * 5
```




    [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]




```python
5 * 'abcd'
```




    'abcdabcdabcdabcdabcd'



### Building Lists of Lists


```python
# Example 2-12
board = [['_'] * 3 for i in range(3)]
board
```




    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]




```python
board[1][2] = 'X'
board
```




    [['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]




```python
# Example 2-13
weird_board = [['_'] * 3] * 3
weird_board
```




    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]




```python
# The tree items are refered to the same object
weird_board[1][2] = '0'
weird_board
```




    [['_', '_', '0'], ['_', '_', '0'], ['_', '_', '0']]




```python
# The problem with Example 2-13 is that, in essence, it behaves like the code:
row = ['_'] * 3
board = []
for i in range(3):
    board.append(row)
# The same row is appended three times to board
id(board[0]) == id(board[1])
```




    True




```python
# On the other hand, the list comprehension from Example 2-12 is equivalent to this code:
board = []
for i in range(3):
    row = ['_'] * 3
    board.append(row)
id(board[0]) == id(board[1])
```




    False



## Augmented Assignment with Sequences
The special method that makes += work is __iadd__ (for "in-place addition"). 

a += b

However. if __iadd__ is not implemented, Python falls back to callling __add__, then:

a += b equals to a = a + b


```python
# In the case of mutable sequences(e.g. list, bytearray, array.array)
l = [1, 2, 3]
id(l)
```




    140365970938568




```python
l *= 2
id(l)
```




    140365970938568




```python
t = (1, 2, 3)
id(t)
```




    140365919599136




```python
t *= 2
id(t)
```




    140365919510344



### A += Assignment Pluzzler


```python
# Example 2-14
t = (1, 2, [30, 40])
t[2] += [50, 60]
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-76-0d38463e151b> in <module>()
          1 # Example 2-14
          2 t = (1, 2, [30, 40])
    ----> 3 t[2] += [50, 60]
    

    TypeError: 'tuple' object does not support item assignment



```python
t
```




    (1, 2, [30, 40, 50, 60])



## List.sort and the sorted Built-in Function
The list.sort method sorts a list in place. It returns None to remind us that it changes the target object, and does not create a new list.

This is an importtant Python API convention: functionsor methods that change an object in pace should return None to make it clear to the caller that the object itself was changed.

In contrast, the built-in function sorted creats a new list and returns it.


```python
fruits = ['grape', 'raspberry', 'apple', 'banana']
sorted(fruits)
```




    ['apple', 'banana', 'grape', 'raspberry']




```python
fruits
```




    ['grape', 'raspberry', 'apple', 'banana']




```python
sorted(fruits, reverse=True)
```




    ['raspberry', 'grape', 'banana', 'apple']




```python
sorted(fruits, key=len)
```




    ['grape', 'apple', 'banana', 'raspberry']




```python
sorted(fruits, key=len, reverse=True)
```




    ['raspberry', 'banana', 'grape', 'apple']




```python
fruits.sort()
```


```python
fruits
```




    ['apple', 'banana', 'grape', 'raspberry']



## Managing Ordered Sequences with bisect
The bisect module offers two main functions-bisect and insort-that use the binary search algorithm to quickly find and insert items in any sorted sequences.

```python
# Example 2-17
import sys
import bisect

HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30 ,31]

ROW_FOMAT = '{0:2d} @ {1:2d}    {2}{0:2d}'

def demo(bisect_fn):
    for needle in reversed(NEEDELS):
        position = bisect_fn(HAYSTACK, needle)
        offset = position * ' |'
        print(ROW_FORMAT.format(needle, position, offset))
        
if __name__ == '__main__':
    if sys.argv[-1] == 'left':
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect
    print('DEMO:', bisect_fn.__name__)
    print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)
```


```python
import bisect
```


```python
HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30 ,31]
# Get the insert position by binary search
position = bisect.bisect(HAYSTACK, 0)
position
```




    0



### Insert with bisect.insort
Sorting is expensive, so once you have a sorted sequence, it's good to keep it that way.

That is why bisect.insort was created.


```python
# Example 2-19
import bisect
import random

SIZE = 7

random.seed(1729)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)
```

    10 -> [10]
     0 -> [0, 10]
     6 -> [0, 6, 10]
     8 -> [0, 6, 8, 10]
     7 -> [0, 6, 7, 8, 10]
     2 -> [0, 2, 6, 7, 8, 10]
    10 -> [0, 2, 6, 7, 8, 10, 10]

