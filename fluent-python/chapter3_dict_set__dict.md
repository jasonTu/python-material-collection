
## Generic Mapping Types
The collections.abc module provides the Mapping and MutableMapping ABCs to formalize the interfaces of dict and similar types.


```python
from collections import abc
my_dict = {}
isinstance(my_dict, abc.Mapping)
```




    True



### What is hashable
An object is hashable if it has a hash value which never changes during its lifetime(it needs  a \__hash__() method), and can be compared to other object(it need an \__eq__() method)

The atomic immutable types(str, bytes, numeric types) are all hashable. A frozen set is always hashable, becauses elements must be hashable by definition.

A tupe is hashable only if all its elements are hashable


```python
tt = (1, 2, (30, 40))
hash(tt)
```




    8027212646858338501




```python
tl = (1, 2, [30, 40])
hash(tl)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-5-258d676ca6dc> in <module>()
          1 tl = (1, 2, [30, 40])
    ----> 2 hash(tl)
    

    TypeError: unhashable type: 'list'



```python
tf = (1, 2, frozenset([30, 40]))
hash(tf)
```




    -4118419923444501110




```python
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('one', 1), ('two', 2), ('three', 3)])
e = dict({'three': 3, 'one': 1, 'two': 2})
a == b == c == d == e
```




    True



## Dict Comprehensions


```python
DIAL_CODES = [
    (86, 'China'),
    (91, 'India'),
    (1, 'United States')
]
country_code = {country: code for code, country in DIAL_CODES}
country_code
```




    {'China': 86, 'India': 91, 'United States': 1}




```python
{code: country.upper() for country, code in country_code.items() if code < 66}
```




    {1: 'UNITED STATES'}



## Mapping with Flexible Key Lookup
Return a make-up value when a missing key is lookup is good. There are two main approaches to this: default dict and "\__missing__" method of plain dict.

### defaultdict
Here is how it works: when instantint a defaultdict, you provide a callable that is used to produce a default value whenever \__getitem__ is passed a nonexist key argument.
    
For example, given an empty defaultdict created as dd = defaultdict(lsit), if 'new-key' is not in dd, the expression dd['new-key'] does the following steps:
* Calls list() to create a new list
* Inserts the listinto dd usin'new-key' as key
* Returns a reference to that list

The callable that prothe default valeus is held in an instance attribute called default_factory.

### The \__mission__ method
Underlying the way mappings deal with missing keys is the aptly named \__missing__ method. 

This method is not defined in the base dict class, but dict is aware of it: if you subclass dict and provide a \__missing__ method, the standard dict

\__getitem__ will call it whenever a key is not found, instead of raising KeyError.


```python
# Example 3-6: When searching for a nontring key, StrKeyDict0 converts it to str when it is not found.
class StrKeyDict0(dict):
    
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
        
    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()
```


```python
d = StrKeyDict0([('2', 'two'), ('4', 'four')])
d['2']
```




    'two'




```python
d[4]
```




    'four'




```python
d[1]
```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-39-abe283337115> in <module>()
    ----> 1 d[1]
    

    <ipython-input-36-ec1abf75f461> in __missing__(self, key)
          5         if isinstance(key, str):
          6             raise KeyError(key)
    ----> 7         return self[str(key)]
          8 
          9     def get(self, key, default=None):


    <ipython-input-36-ec1abf75f461> in __missing__(self, key)
          4     def __missing__(self, key):
          5         if isinstance(key, str):
    ----> 6             raise KeyError(key)
          7         return self[str(key)]
          8 


    KeyError: '1'



```python
d.get('2')
```




    'two'




```python
d.get(4)
```




    'four'




```python
d.get(1, 'N/A')
```




    'N/A'




```python
2 in d
```




    True




```python
1 in d
```




    False



### Variations of dict
* collections.OrderedDict
* collections.ChainMap
* collections.Counter
* collections.UserDict

While OrderedDcit, ChainMap and Counter come ready to use, UserDict is designed to be subclassed.

### Subclassing UserDict


```python
# Example 3-8 StrKeyDict always convert non-string keys to str-on inserting, update and lookup
import collections

class StrKeyDict(collections.UserDict):
    
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data
    
    def __setitem__(self, key, item):
        self.data[str(key)] = item
```


```python
### Immutable Mappings
from types import MappingProxyType
d = {1: 'A'}
d_proxy = MappingProxyType(d)
d_proxy
```




    mappingproxy({1: 'A'})




```python
d_proxy[1]
```




    'A'




```python
d_proxy[1] = 'x'
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-49-b51dbd977dee> in <module>()
    ----> 1 d_proxy[1] = 'x'
    

    TypeError: 'mappingproxy' object does not support item assignment



```python
d[2] = 3
d_proxy
```




    mappingproxy({1: 'A', 2: 3})


