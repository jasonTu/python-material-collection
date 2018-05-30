
## Decorators 101
A decorator is a callable that takes another function as argument (the decorated func‐ tion) The decorator may perform some processing with the decorated function, and returns it or replaces it with another function or callable object.


```python
# Example 7-1: A decorator usually replaces a function with a different one
def deco(func):
    def inner():
        print('running inner()')
    return inner

# target = deco(target)
@deco
def target():
    print('running target()')
```


```python
target()
```

    running inner()



```python
target
```




    <function __main__.deco.<locals>.inner()>



## Why Python Executes Decorators
A key feature of decorators is that they run right after the decorated function is defined. That is usually at import time (i.e., when a module is loaded by Python). Consider registration.py in Example 7-2.


```python
# Example 7-2: The registration module
registry = []

def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')
    
@register
def f2():
    print('running f2()')
    
def f3():
    print('running f3()')
```

    running register(<function f1 at 0x106275048>)
    running register(<function f2 at 0x106311d08>)



```python
registry
```




    [<function __main__.f1()>, <function __main__.f2()>]




```python
f1()
```

    running f1()



```python
f2()
```

    running f2()



```python
f3()
```

    running f3()


## Decorator-Enhanced Strategy Pattern


```python
# Exmaple 7-3: The promos list is filled by the promotion decorator
promos = []

def promotion(promo_func):
    promos.append(promo_func)
    return promo_func

@promotion
def fidelity(order):
    '''5% discount for customers with 1000 or more fidelity points'''
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion
def bulk_item(order):
    '''10% discount for each LineItem with 20 or more units'''
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

@promotion
def large_order(order):
    '''7% discount for orders with 10 or more distinct items'''
    dictinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

def best_promo(order):
    '''Select best discount available'''
    return max(promo(order) for promo in promos)
```

## Variable Scope Rules
In Example 7-4, we define and test a function that reads two variables: a local variable a, defined as function parameter, and variable b that is not defined anywhere in the function.


```python
# Example 7-4: Function reading a local and global variable
def f1(a):
    print(a)
    print(b)
```


```python
f1(3)
```

    3



    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-17-db0f80b394ed> in <module>()
    ----> 1 f1(3)
    

    <ipython-input-16-b86a5b369635> in f1(a)
          2 def f1(a):
          3     print(a)
    ----> 4     print(b)
    

    NameError: name 'b' is not defined



```python
b = 6
f1(3)
```

    3
    6



```python
# Example 7-5. Variable b is local, because it is assigned a value in the body of the function
b = 6
def f2(a):
    print(a)
    print(b)
    b = 9
```


```python
f2(3)
```

    3



    ---------------------------------------------------------------------------

    UnboundLocalError                         Traceback (most recent call last)

    <ipython-input-22-ddde86392cb4> in <module>()
    ----> 1 f2(3)
    

    <ipython-input-21-b63070679a0f> in f2(a)
          3 def f2(a):
          4     print(a)
    ----> 5     print(b)
          6     b = 9


    UnboundLocalError: local variable 'b' referenced before assignment



```python
def f3(a):
    global b
    print(a)
    print(b)
    b = 9
```


```python
f3(3)
```

    3
    6


## Cloures
Actually, a closure is a function with an extended scope that encompasses nonglobal variables referenced in the body of the function but not defined there. It does not matter whether the function is anonymous or not; what matters is that it can access nonglobal variables that are defined outside of its body.


```python
# Example 7-8: A class to calculate a running average.
class Averager():
    
    def __init__(self):
        self.series = []
        
    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)
```


```python
avg = Averager()
```


```python
avg(10)
```




    10.0




```python
avg(11)
```




    10.5




```python
avg(12)
```




    11.0




```python
# Example 7-9: A higher-order function to calculate a running average
def make_averager():
    series = []
    
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager
```


```python
avg = make_averager()
```


```python
avg(10)
```




    10.0




```python
avg(11)
```




    10.5




```python
avg(12)
```




    11.0



### Description of example 7-9
Note that series is a local variable of make_averager because the initialization series = [] happens in the body of that function. But when avg(10) is called, make_averager has already returned, and its local scope is long gone.
Within averager, series is a free variable. This is a technical term meaning a variable that is not bound in the local scope.

The closure for averager extends the scope of that function to include the binding for the free variable series.

Inspecting the returned averager object shows how Python keeps the names of local and free variables in the __code__ attribute that represents the compiled body of the function. Example 7-11 demonstrates.


```python
# Example 7-11: Inspecting the function created by make_average.
avg.__code__.co_varnames
```




    ('new_value', 'total')




```python
avg.__code__.co_freevars
```




    ('series',)



The binding for series is kept in the \__closure__ attribute of the returned function avg. Each item in avg.\__closure__ corresponds to a name in avg.\__code__.co_free vars. These items are cells, and they have an attribute called cell_contents where the actual value can be found. 


```python
avg.__closure__
```




    (<cell at 0x1062a5678: list object at 0x106163708>,)




```python
avg.__closure__[0].cell_contents
```




    [10, 11, 12]



To summarize: a closure is a function that retains the bindings of the free variables that exist when the function is defined, so that they can be used later when the function is invoked and the defining scope is no longer available.

## The nonlocal Declaration


```python
# Example 7-13: A broken higher-order function to calculate a running average without keeping all history
def make_averager():
    count = 0
    total = 0
    
    def averager(new_value):
        # The problem is: below statement count += 1 actually means count = count + 1, when count is immutable type
        count += 1
        total += new_value
        return total / count
    return averager
```


```python
avg = make_averager()
```


```python
avg(10)
```


    ---------------------------------------------------------------------------

    UnboundLocalError                         Traceback (most recent call last)

    <ipython-input-53-ace390caaa2e> in <module>()
    ----> 1 avg(10)
    

    <ipython-input-51-f94b29bf899a> in averager(new_value)
          5 
          6     def averager(new_value):
    ----> 7         count += 1
          8         total += new_value
          9         return total / count


    UnboundLocalError: local variable 'count' referenced before assignment


We did not have this problem in Example 7-9 because we never assigned to the ser ies name; we only called series.append and invoked sum and len on it. So we took advantage of the fact that lists are mutable.

But with immutable types like numbers, strings, tuples, etc., all you can do is read, but never update. If you try to rebind them, as in count = count + 1, then you are implicitly creating a local variable count. It is no longer a free variable, and therefore it is not saved in the closure.

To work around this, the nonlocal declaration was introduced in Python 3. It lets you flag a variable as a free variable even when it is assigned a new value within the function. If a new value is assigned to a nonlocal variable, the binding stored in the closure is changed. A correct implementation of our newest make_averager looks like Example 7-14.


```python
# Example 7-14: Calculate a running average without keeping all history(fixed with the use of nonlocal)
def make_averager():
    count = 0
    total = 0
    
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    
    return averager
```


```python
avg = make_averager()
avg(10)
```




    10.0


