
## Implementing a Simple Decorator


```python
# Example 7-15: A simple decorator to output the running time of functions
import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
```


```python
# Example 7-16: Using the clock decorator
import time

@clock
def snooze(seconds):
    time.sleep(seconds)
    
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)
```


```python
snooze(.123)
```

    [0.12721738s] snooze(0.123) -> None



```python
factorial(6)
```

    [0.00000081s] factorial(1) -> 1
    [0.00032174s] factorial(2) -> 2
    [0.00038944s] factorial(3) -> 6
    [0.00044612s] factorial(4) -> 24
    [0.00049986s] factorial(5) -> 120
    [0.00055287s] factorial(6) -> 720





    720



### How it Works
Remember that this code:

```python
@clock
def factorial(n):
    return 1 if n < 2 else n*facotiral(n-1)
```

Actually does this:

```python
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

factorial = clock(factorial)
```


```python
# function attribute changes
factorial.__name__
```




    'clocked'



This is the typical behavior of a decorator: it replaces the decorated function with a new function that accepts the same arguments and (usually) returns whatever the decorated function was supposed to return, while also doing some extra processing.

The clock decorator implemented in Example 7-15 has a few shortcomings: it does not support keyword arguments, and it masks the __name__ and __doc__ of the decorated function. Example 7-17 uses the functools.wraps decorator to copy the relevant at‐ tributes from func to clocked. Also, in this new version, keyword arguments are cor‐ rectly handled.


```python
# Example 7-17: An improved clock decorator
import time
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, v) for k, v in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
```


```python
@clock
def paramed_func(*args, **kwargs):
    return None
```


```python
paramed_func((1, 2, 3), a=1, b=2, c=3)
```

    ['(1, 2, 3)', 'a=1, b=2, c=3']
    [0.00000286s] paramed_func((1, 2, 3), a=1, b=2, c=3) -> None



```python
paramed_func.__code__.co_freevars
```




    ('func',)



## Decorators in the Standard Library
Python has three built-in functions that are designed to decorate methods: property, classmethod, and staticmethod. 

Another frequently seen decorator is functools.wraps, a helper for building well- behaved decorators. We used it in Example 7-17. Two of the most interesting decorators in the standard library are lru_cache and the brand-new singledispatch (added in Python 3.4). Both are defined in the functools module. We’ll cover them next.

### Memorization with functools.lru_cache
A very practical decorator is functools.lru_cache. It implements memoization: an optimization technique that works by saving the results of previous invocations of an expensive function, avoiding repeat computations on previously used arguments. The letters LRU stand for Least Recently Used, meaning that the growth of the cache is limited by discarding the entries that have not been read for a while.


```python
# Example 7-18: The very costly recusive way to compute the nth number in the Fibonacci series
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
```


```python
print(fibonacci(6))
```

    [0.00000095s] fibonacci(0) -> 0
    [0.00000310s] fibonacci(1) -> 1
    [0.00043797s] fibonacci(2) -> 1
    [0.00000191s] fibonacci(1) -> 1
    [0.00000191s] fibonacci(0) -> 0
    [0.00000215s] fibonacci(1) -> 1
    [0.00019789s] fibonacci(2) -> 1
    [0.00151205s] fibonacci(3) -> 2
    [0.00216484s] fibonacci(4) -> 3
    [0.00000119s] fibonacci(1) -> 1
    [0.00000072s] fibonacci(0) -> 0
    [0.00000095s] fibonacci(1) -> 1
    [0.00009894s] fibonacci(2) -> 1
    [0.00019979s] fibonacci(3) -> 2
    [0.00000095s] fibonacci(0) -> 0
    [0.00000119s] fibonacci(1) -> 1
    [0.00012112s] fibonacci(2) -> 1
    [0.00000095s] fibonacci(1) -> 1
    [0.00000191s] fibonacci(0) -> 0
    [0.00000119s] fibonacci(1) -> 1
    [0.00011396s] fibonacci(2) -> 1
    [0.00022697s] fibonacci(3) -> 2
    [0.00045323s] fibonacci(4) -> 3
    [0.00075603s] fibonacci(5) -> 5
    [0.00304008s] fibonacci(6) -> 8
    8


The waste is obvious: fibonacci(1) is called eight times, fibonacci(2) five times, etc. But if we just add two lines to use lru_cache, performance is much improved. See Example 7-19.


```python
# Example 7-19: Faster implementation using caching
import functools

@functools.lru_cache() # Note 1
@clock # Note 2
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
```


```python
fibonacci(6)
```

    [0.00000000s] fibonacci(0) -> 0
    [0.00000215s] fibonacci(1) -> 1
    [0.00039506s] fibonacci(2) -> 1
    [0.00000191s] fibonacci(3) -> 2
    [0.00049877s] fibonacci(4) -> 3
    [0.00000095s] fibonacci(5) -> 5
    [0.00058794s] fibonacci(6) -> 8





    8



Note:
* Note that lru_cache must be invoked as a regular function—note the parentheses in the line: @functools.lru_cache(). The reason is that it accepts configuration parameters, as we’ll see shortly.
* This is an example of stacked decorators: @lru_cache() is applied on the function returned by @clock.

```python
functools.lru_cache(maxsize=128, typed=False)
```

The maxsize argument determines how many call results are stored. After the cache is full, older results are discarded to make room. For optimal performance, maxsize should be a power of 2. The typed argument, if set to True, stores results of different argument types separately, i.e., distinguishing between float and integer arguments that are nor‐ mally considered equal, like 1 and 1.0. By the way, because lru_cache uses a dict to store the results, and the keys are made from the positional and keyword arguments used in the calls, all the arguments taken by the decorated function must be hashable.

## Stacked Decorators
Example 7-19 demonstrated the use of stacked decorators: @lru_cache is applied on the result of @clock over fibonacci. In Example 7-21, the @htmlize.register deco‐ rator was applied twice to the last function in the module.

When two decorators @d1 and @d2 are applied to a function f in that order, the result is the same as f = d1(d2(f)).

In other words, this:

```python
@d1
@d2
def f():
    print('f')
```

Is the same as:

```python
def f():
    print('f')
f = d1(d2(f))
```

## Parametered Decorators
When parsing a decorator in source code, Python takes the decorated function and passes it as the first argument to the decorator function. So how do you make a decorator accept other arguments? The answer is: make a decorator factory that takes those ar‐ guments and returns a decorator, which is then applied to the function to be decorated. Confusing? Sure. Let’s start with an example based on the simplest decorator we’ve seen: register in Example 7-22.


```python
# Example 7-22
registry = []

def register(func):
    print('running register (%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')
```

    running register (<function f1 at 0x10ea029d8>)



```python
registry
```




    [<function __main__.f1()>]




```python
f1()
```

    running f1()


### A Parameterized Registration Decorator


```python
# Example 7-23: To accept parameters, the new register decorator must be called as a function
registry = set()

def register(active=True):
    def decorate(func):
        print('running register(active=%s)->decorate(%s)' % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
            
        return func
    return decorate
```


```python
@register(active=False)
def f1():
    print('running f1()')
```

    running register(active=False)->decorate(<function f1 at 0x10eaa3730>)



```python
registry
```




    set()




```python
@register()
def f2():
    print('running f2()')
```

    running register(active=True)->decorate(<function f2 at 0x10eaa3598>)



```python
registry
```




    {<function __main__.f2()>}




```python
def f3():
    print('running f3()')
```


```python
register()(f3)
```

    running register(active=True)->decorate(<function f3 at 0x10ea97048>)





    <function __main__.f3()>




```python
registry
```




    {<function __main__.f2()>, <function __main__.f3()>}



### The Parameterized Clock Decorator


```python
# Example 7-25: The parameterized clock decorator
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args} -> {result})'

def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate
```


```python
@clock()
def snooze(seconds):
    time.sleep(seconds)
```


```python
snooze(.123)
```

    [0.12407184s] snooze(0.123 -> None)



```python
@clock('{name}: {elapsed}s')
def snooze(seconds):
    time.sleep(seconds)
```


```python
snooze(.123)
```

    snooze: 0.12631702423095703s

