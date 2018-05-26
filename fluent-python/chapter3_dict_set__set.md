
## Set Theory

### Set Literals
The syntax of set literals—{1}, {1, 2}, etc.—looks exactly like the math notation.

With one important exception: there’s no literal notation for the empty set, so we must remember to write set().


```python
s = {1}
type(s)
```




    set




```python
s
```




    {1}




```python
from dis import dis
dis('{1}')
```

      1           0 LOAD_CONST               0 (1)
                  3 BUILD_SET                1
                  6 RETURN_VALUE



```python
dis('set([1])')
```

      1           0 LOAD_NAME                0 (set)
                  3 LOAD_CONST               0 (1)
                  6 BUILD_LIST               1
                  9 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
                 12 RETURN_VALUE


### Set Comprehensions


```python
from unicodedata import name
{chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}
```




    {'#',
     '$',
     '%',
     '+',
     '<',
     '=',
     '>',
     '¢',
     '£',
     '¤',
     '¥',
     '§',
     '©',
     '¬',
     '®',
     '°',
     '±',
     'µ',
     '¶',
     '×',
     '÷'}



### Set Operations

### dict and set Under the Hood
Understanding how Python dictionaries and sets implemented using hash tables is helpful to make sense of their strenths and limitations.

## Practical Consequences of How dict works

### Keys must be hashable objects
* It supports the hash() function via a hash() method that always returns the same value over the lifetime of the object.
* It supports equality via an eq() method.
* If a == b is True then hash(a) == hash(b) must also be True.

User-defined types are hashable by default because their hash value is their id() and they all compare not equal
* if \__eq__ is implemented, then must implement suitable \__hash__ method to make sure a == b and hash(a) == hash(b)

### dict have significant memory overhead
Because a dict uses a hash table internally. you hash table must be sparse to work, they are not space efficient.

Optimize it in need, use tuple or list instead.

### Key search is very fast

### Key ordering depends on inserting order


```python
# Example 3-17
DIAL_CODES = [
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
    (62, 'Indonesia'),
    (55, 'Brazil'),
    (92, 'Pakistan'),
    (880, 'Bangladesh'),
    (234, 'Nigeria'),
    (7, 'Russia'),
    (81, 'Japan'),
]
d1 = dict(DIAL_CODES)
print('d1:', d1.keys())
```

    d1: dict_keys([880, 1, 86, 55, 7, 234, 91, 92, 62, 81])



```python
d2 = dict(sorted(DIAL_CODES))
print('d2:', d2.keys())
```

    d2: dict_keys([880, 1, 91, 86, 81, 55, 234, 7, 92, 62])



```python
d3 = dict(sorted(DIAL_CODES, key=lambda x:x[1]))
print('d3:', d3.keys())
```

    d3: dict_keys([880, 81, 1, 86, 55, 7, 234, 91, 92, 62])



```python
assert d1 == d2 and d2 == d3
```

### Adding items to a dict may change the order of existing keys

## How Sets Work--Practical Consequences
* Set elements must be hashable objects.
* Sets have a significant memory overhead.
* Membership testing is very efficient.
* Element ordering depends on insertion order
* Adding elements to a set may change the order of other elements.
