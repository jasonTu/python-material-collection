
## del and Garbage Collection
The del statement deletes names, not objects. An object may be garbage collected as result of a del command, but only if the variable deleted holds the last reference to the object, or if the object becomes unreachable.2 Rebinding a variable may also cause the number of references to an object to reach zero, causing its destruction.

To demonstrate the end of an object’s life, Example 8-16 uses weakref.finalize to register a callback function to be called when an object is destroyed.


```python
# Example 8-6: Watching the end of an object when no more references point to it
import weakref
s1 = {1, 2, 3}
s2 = s1
def bye():
    print('Gone with the wind...')

# Register the bye callback on the object referred by s1.
ender = weakref.finalize(s1, bye)
# Rebinding the last reference, s2, makes {1, 2, 3} unreachable. 
# It is destroyed, the bye callback is invoked, and ender.alive becomes False.
ender.alive
```




    True




```python
del s1
```


```python
ender.alive
```




    True




```python
s2 = 'spam'
```

    Gone with the wind...



```python
ender.alive
```




    False



## Weak Reference
The presence of references is what keeps an object alive in memory. When the reference count of an object reaches zero, the garbage collector disposes of it. But sometimes it is useful to have a reference to an object that does not keep it around longer than necessary. A common use case is a cache.

Weak references to an object do not increase its reference count. The object that is the target of a reference is called the referent. Therefore, we say that a weak reference does not prevent the referent from being garbage collected.

Weak references are useful in caching applications because you don’t want the cached objects to be kept alive just because they are referenced by the cache.


```python
import weakref
a_set = {0, 1}
wref = weakref.ref(a_set)
wref
```




    <weakref at 0x1108ad368; to 'set' at 0x11015e2e8>




```python
# Invoking wref() returns the referenced object, {0, 1}. Because this is a console
# session, the result {0, 1} is bound to the _ variable.
wref()
```




    {0, 1}




```python
a_set = {2, 3, 4}
```


```python
wref()
```




    {0, 1}




```python
wref() is None
```




    False




```python
wref() is None
```




    False



### The WeakValueDictionary Skit
The class WeakValueDictionary implements a mutable mapping where the values are weak references to objects. When a referred object is garbage collected elsewhere in the program, the corresponding key is automatically removed from WeakValueDiction ary. This is commonly used for caching.


```python
# Example 8-18: Cheese has a kind attribute and a standard representation
class Cheese:
    
    def __init__(self, kind):
        self.kind = kind
    
    def __repr__(self):
        return 'Cheese(%r)' % self.kind
```


```python
# Example 8-19: Customer: "Have you in fact got any cheese here at all?"
import weakref
stock = weakref.WeakValueDictionary()
catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]

for cheese in catalog:
    stock[cheese.kind] = cheese

sorted(stock.keys())
```




    ['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']




```python
del catalog
```


```python
# stock[cheese.kind] = cheese in the for loop; the cheese object's scope is not just in for loop
# Actually the cheese variable is s global variable
sorted(stock.keys())
```




    ['Parmesan']




```python
# After del cheese, all object in catalog are garbage collected
del cheese
sorted(stock.keys())
```




    []



### Limitations of Weak References
Not every Python object may be the target, or referent, of a weak reference. Basic list and dict instances may not be referents, but a plain subclass of either can solve this problem easily:


```python
class MyList(list):
    '''List subclass whose instances may be weakly referenced.'''
    pass
```


```python
a_list = MyList(range(10))
wref_to_a_list = weakref.ref(a_list)
```

A set instance can be a referent, and that’s why a set was used in Example 8-17. User- defined types also pose no problem, which explains why the silly Cheese class was needed in Example 8-19. But int and tuple instances cannot be targets of weak refer‐ ences, even if subclasses of those types are created.
Most of these limitations are implementation details of CPython that may not apply to other Python iterpreters. They are the result of internal optimizations, some of which are discussed in the following (highly optional) section.
