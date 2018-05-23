
## Class for With
```python
class controlled_execution:
        def __enter__(self):
            set things up
            return thing
        def __exit__(self, type, value, traceback):
            tear things down

    with controlled_execution() as thing:
         some code
```


```python
class CE:
    def __enter__(self):
        print('In enter')
        return 2
    def __exit__(self, type, value, traceback):
        print('In exit')
```


```python
with CE() as ce:
    print(ce)
```

    In enter
    2
    In exit


## Function for With
```python
from contextlib import contextmanager

@contextmanager
def control_execution():
    set things up
    yield thing
    tear things down
```


```python
from contextlib import contextmanager

@contextmanager
def control_execution2():
    print('In enter')
    yield 1
    print('In exit')
```


```python
with control_execution2() as ce:
    print(ce)
```

    In enter
    1
    In exit

