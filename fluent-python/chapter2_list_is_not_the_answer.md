
## When a List is not the Answer

### Arrays
A Python array is as lean as C array.


```python
# Example 2-20
from array import array
from random import random
floats = array('d', (random() for i in range(10**7)))
floats[-1]
```




    0.6840540276188549




```python
with open('chapter2/floats.bin', 'wb') as fp:
    floats.tofile(fp)
```


```python
floats2 = array('d')
with open('chapter2/floats.bin', 'rb') as fp:
    floats2.fromfile(fp, 10**7)
```


```python
floats2[-1]
```




    0.6840540276188549




```python
floats2 == floats
```




    True



### Memory Views


```python
# Example 2-21: Changing the value of an array item by poking one of its bytes
numbers = array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)
len(memv)
```




    5




```python
memv[0]
```




    -2




```python
memv_oct = memv.cast('B')
memv_oct.tolist()
```




    [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]




```python
memv_oct[5] = 4
numbers
```




    array('h', [-2, -1, 1024, 1, 2])



### NumPy and SciPy


```python
# Example 2-22: Basic operations with rows and columns in a numpy.ndarray
import numpy
a = numpy.arange(12)
a
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])




```python
type(a)
```




    numpy.ndarray




```python
a.shape
```




    (12,)




```python
a.shape = 3, 4
```


```python
a
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]])




```python
a[:, 1]
```




    array([1, 5, 9])




```python
a.transpose()
```




    array([[ 0,  4,  8],
           [ 1,  5,  9],
           [ 2,  6, 10],
           [ 3,  7, 11]])



### Deques and Other Queues
The class collections.deque is a thread-safe double-ended queue designed for fast inserting and removing from both ends.


```python
# Example 2-23
from collections import deque
dq = deque(range(10), maxlen=10)
dq
```




    deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])




```python
dq.rotate(3)
dq
```




    deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6])




```python
dq.appendleft(-1)
dq
```




    deque([-1, -1, 7, 8, 9, 0, 1, 2, 3, 4])




```python
dq.extend([11, 12, 33])
dq
```




    deque([8, 9, 0, 1, 2, 3, 4, 11, 12, 33])




```python
dq.extendleft([10, 20, 30, 40])
dq
```




    deque([40, 30, 20, 10, 8, 9, 0, 1, 2, 3])


