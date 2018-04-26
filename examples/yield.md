
## 当我们调用yield，它究竟做了什么
显然，要理解yield，首先要了解迭代器（iterator），接着了解什么是生成器(generator)。

### 迭代器
通俗的讲，迭代器就是可以逐个访问的容器，而逐个逐步访问的过程成为迭代。


```python
iterator = [item for item in range(5)]
for i in iterator:
    print(i)
```

    0
    1
    2
    3
    4


### 生成器
上述代码中，iterator就是一个迭代器，for循环部分就是迭代过程。生成器同样也是可供迭代访问的容器，与迭代器不同的是，生成器中的元素不会一次性存入内润中，而是一边迭代一边生成。


```python
generator = (item for item in range(5))
for i in generator:
    print(i)
```

    0
    1
    2
    3
    4


### 迭代器和生成器的执行效率
因为生成器边迭代边生成，所以占用内存极少，执行效率也更高。


```python
def go_thru_iterator(item_len):
    iterator = [item for item in range(item_len)]
    for i in iterator:
        pass
```


```python
def go_thru_generator(item_len):
    generator = (item for item in range(item_len))
    for i in generator:
        pass
```


```python
%time go_thru_iterator(100000000)
```

    CPU times: user 12 s, sys: 11.8 s, total: 23.8 s
    Wall time: 23.8 s



```python
%time go_thru_generator(100000000)
```

    CPU times: user 12.7 s, sys: 0 ns, total: 12.7 s
    Wall time: 12.6 s


### yield
yield的使用和return的使用没有什么区别，只是yield会返回一个生成器。当代码执行到yield时，该函数会返回yield之后的值，并在原地等待下一次迭代；当执行到下一次迭代时，代码接着上一次等待的地方执行：
* 若使用生成器的send方法，则yield语句的返回值send中的参数
* 若使用next函数迭代，则在yield的返回值为None


注： next相当于mgen.send(None)，但mgen.send在生成器第一次迭代时不可调用


```python
def create_generator():
    mylist = range(3)
    for i in mylist:
        ret = yield i * i
        print('ret:', ret)
```


```python
mgen = create_generator()
```


```python
next(mgen)
```




    0




```python
next(mgen)
```

    ret: None





    1




```python
mgen.send('The yield return value.')
```

    ret: The yield return value.





    4




```python
try:
    next(mgen)
except StopIteration:
    print('Already arrive the end of the generator element.')
```

    ret: None
    Already arrive the end of the generator element.

