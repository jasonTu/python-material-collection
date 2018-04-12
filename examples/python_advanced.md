
## Referer
* [Python高级编程](http://www.iqiyi.com/w_19ru9hbjil.html)

### 变量


```python
d = {'a': 1, 'b': 2}
```


```python
for k, v in d.iteritems():
    exec '{}={}'.format(k, v)
```


```python
a
```




    1




```python
b
```




    2




```python
globals().update(d)
```


```python
d
```




    {'a': 1, 'b': 2}




```python
'a'
```




    'a'




```python
globals()['a'] = 'b'
```


```python
a
```




    'b'




```python
vars() is locals()
```




    True




```python
import sys
vars(sys) is sys.__dict__
```




    True



### 字符串格式化


```python
import datetime
```


```python
'Today is: {0:%a %b %d %H:%M:%S %Y}'.format(datetime.datetime.now())
```




    'Today is: Wed Mar 28 16:26:19 2018'



### 列表去重


```python
l = [1, 2, 2, 3, 3, 3]
```


```python
# Used in python2
{}.fromkeys(l).keys()
```




    [1, 2, 3]




```python
# Common ways to remove duplicate items
list(set(l))
```




    [1, 2, 3]




```python
# 操作字典
```


```python
dict((['a', 1], ['b', 2]))
```




    {'a': 1, 'b': 2}




```python
dict(zip('ab', range(2)))
```




    {'a': 0, 'b': 1}




```python
zip('ab', range(2))
```




    [('a', 0), ('b', 1)]




```python
dict.fromkeys('abc', 1)
```




    {'a': 1, 'b': 1, 'c': 1}




```python
d.setdefault('a', 100)
```




    1




```python
d.setdefault('c', 100)
```




    100




```python
d1 = dict(a=1, b=2)
```


```python
d1
```




    {'a': 1, 'b': 2}




```python
d2 = dict(b=2, c=2)
```


```python
d2
```




    {'b': 2, 'c': 2}




```python
d1 & d2
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-42-0465179a342a> in <module>()
    ----> 1 d1 & d2
    

    TypeError: unsupported operand type(s) for &: 'dict' and 'dict'



```python
v1 = d1.viewitems()
```


```python
v1
```




    dict_items([('a', 1), ('b', 2)])




```python
v2 = d2.viewitems()
```


```python
v2
```




    dict_items([('c', 2), ('b', 2)])




```python
v1 & v2
```




    {('b', 2)}




```python
dict(v1 & v2)
```




    {'b': 2}




```python
v1 | v2
```




    {('a', 1), ('b', 2), ('c', 2)}




```python
dict(v1 | v2)
```




    {'a': 1, 'b': 2, 'c': 2}




```python
v1 - v2
```




    {('a', 1)}




```python
dict(v1 - v2)
```




    {'a': 1}



### 迭代器和生成器
迭代器协议
* 迭代器协议是指：对象需要提供next方法，它要么返回迭代中的下一项，要么就引起一个StopIteration异常，以终止迭代 
* 可迭代对象就是：实现了迭代器协议的对象 

生成器
* 生成器函数：常规函数定义，但是，使用yield语句而不是return语句返回结果。yield语句一次返回一个结果，在每个结果中间，挂起函数的状态，以便下次重它离开的地方继续执行
* 生成器表达式：类似于列表推导，但是，生成器返回按需产生结果的一个对象，而不是一次构建一个结果列表
* 生成器只能遍历一次

[定义参考](https://www.zhihu.com/question/20829330)


```python
# 写一个简单的迭代器
class Data(object):
    def __init__(self):
        self._data = []
    def add(self, x):
        self._data.append(x)
    def data(self):
        return iter(self._data)

d = Data()
d.add(1)
d.add(2)
d.add(3)
for x in d.data():
    print(x)
```

    1
    2
    3



```python
# 标准迭代器
class Data(object):
    def __init__(self, *args):
        self._data = list(args)
        self._index = 0
    def __iter__(self):
        return self
    # 兼容python3
    def __next__(self):
        return self.next()
    def next(self):
        if self._index >= len(self._data):
            raise StopIteration()
        d = self._data[self._index]
        self._index += 1
        return d

d = Data(1, 2, 3)
for x in d:
    print(x)
```

    1
    2
    3



```python
d.next()
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    <ipython-input-63-c21d42f35a03> in <module>()
    ----> 1 d.next()
    

    <ipython-input-62-d2f3cd432333> in next(self)
         11     def next(self):
         12         if self._index >= len(self._data):
    ---> 13             raise StopIteration()
         14         d = self._data[self._index]
         15         self._index += 1


    StopIteration: 



```python
# 生成器
class Data(object):
    def __init__(self, *args):
        self._data = list(args)
    def __iter__(self):
        for x in self._data:
            yield x

d = Data(1, 2, 3)
for x in d:
    print(x)
```

    1
    2
    3



```python
# 生成器表达式
(i for i in [1, 2, 3])
```




    <generator object <genexpr> at 0x00000000061EBAB0>




```python
# 生成器版斐波那契数列
import itertools
def fib():
    a, b = 0, 1
    while 1:
        yield b
        a, b = b, a + b

print list(itertools.islice(fib(), 10))
```

    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]



```python
help(itertools.islice)
```

    Help on class islice in module itertools:
    
    class islice(__builtin__.object)
     |  islice(iterable, [start,] stop [, step]) --> islice object
     |  
     |  Return an iterator whose next() method returns selected values from an
     |  iterable.  If start is specified, will skip all preceding elements;
     |  otherwise, start defaults to zero.  Step defaults to one.  If
     |  specified as another value, step determines how many values are 
     |  skipped between successive calls.  Works like a slice() on a list
     |  but returns an iterator.
     |  
     |  Methods defined here:
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  next(...)
     |      x.next() -> the next value, or raise StopIteration
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  __new__ = <built-in method __new__ of type object>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
    


### yeild和协程的关系


```python
def coroutine():
    print('Coroutine start...')
    result = None
    while True:
        s = yield result
        result = 'result: {}'.format(s)
```


```python
c = coroutine()
```


```python
c.send(None)
```

    Coroutine start...



```python
c.send('first')
```




    'result: first'




```python
c.send('second')
```




    'result: second'




```python
c.close()
```


```python
c.send('again')
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    <ipython-input-83-366be2d8d7f0> in <module>()
    ----> 1 c.send('again')
    

    StopIteration: 


### 回调


```python
def framework(logic, callback):
    s = logic()
    print('[FX] logic: {}'.format(s))
    print('[FX] do something')
    callback('async: {}'.format(s))

def logic():
    s = 'mylogic'
    return s

def callback(s):
    print(s)
```


```python
framework(logic, callback)
```

    [FX] logic: mylogic
    [FX] do something
    async: mylogic



```python
# next运行到"r = yield s"，返回s，然后切换到调用函数栈，等待发送send，logic协程接受到send之后，r的值被send的参数赋值，指令继续向下执行
def framework(logic):
    try:
        it = logic()
        s = next(it)
        print('[FX] logic: {}'.format(s))
        print('[FX] do something')
        it.send('async: {}'.format(s))
    except StopIteration:
        pass
    
def logic():
    s = 'mylogic'
    r = yield s
    print(r)
```


```python
framework(logic)
```

    [FX] logic: mylogic
    [FX] do something
    async: mylogic


### 上下文管理器contextmanager

语法：
```python
def some_generator(<argument>):
    <setup>
    try:
        yield <value>
    finally:
        <cleanup>
with some_generator(<arguments>) as <variable>:
    <body>

# 以上语法的解释：
<setup>
try:
    <variable> = <value>
    <body>
finally:
    <cleanup>
```


```python
# example
import threading
from contextlib import contextmanager

lock = threading.Lock()
@contextmanager
def openlock():
    print('Acquire')
    lock.acquire()
    yield
    print('Releasing')
    lock.release()

with openlock():
    print('Lock is locked: {}'.format(lock.locked()))
    print('Do some stuff')
```

    Acquire
    Lock is locked: True
    Do some stuff
    Releasing



```python
# another example
@contextmanager
def openlock2():
    print('Acquire')
    with lock:
        yield
    print('Releasing')

with openlock2():
    print('Lock is locked: {}'.format(lock.locked()))
    print('Do some stuff')
```

    Acquire
    Lock is locked: True
    Do some stuff
    Releasing



```python
# at 42:32 in the vedio
```

### 包导入


```python
import imp
```


```python
f, filename, description = imp.find_module('sys')
```


```python
sys = imp.load_module('sys', f, filename, description)
```


```python
sys
```




    <module 'sys' (built-in)>




```python
os = __import__('os')
```


```python
os.path
```




    <module 'ntpath' from 'c:\python27\lib\ntpath.pyc'>




```python
filename = 'test.py'
```


```python
f = open(filename)
```


```python
description = ('.py', 'U', 1)
```


```python
t = imp.load_module('some', f, filename, description)
```


```python
t
```




    <module 'some' from 'test.py'>



### 包创建__all__
因为import实际导入的是目标模块globals名字空间中的成员，那么就要一个问题：模块也会导入其他模块，这些模块同样在目标模块的名字空间中。在进行“import *”操作时，所有这些一并被带入到当前模块中，造成符号污染：

__all__ = ['add', 'x']

### 包构建__path__
某些时候，保内的文件太多， 需要分类存放到多个目录中，但又不想拆分成新的包或子包。这么做是允许的，只要在__init__.py中用__path__指定所有子目录的全路径即可（子目录可放在包外）

➜  python_pkg tree

.

├── a

│   └── add.py

├── b

│   └── sub.py

└── __init.py

```python
from os.path import abspath, join
subdirs = lambda *dirs: [abspath(join(__path__[0], sub)) for sub in dirs]
__path__ = subdirs('a', 'b')

```

#### 参考
* [Python中的 __all__和__path__ 解析](https://blog.csdn.net/u012450329/article/details/53001071)

#### 例子
```python
➜  /tmp tree sound
sound
├── fuzz
│   ├── __init__.py
│   └── __init__.pyc
├── __init__.py
├── __init__.pyc
└── utils
    ├── boss.py
    ├── echo.py
    ├── echo.pyc
    ├── __init__.py
    ├── __init__.pyc
    ├── linux
    │   ├── echo.py
    │   └── echo.pyc
    ├── sonic.py
    └── windows
        └── echo.py

4 directories, 13 files

# __all__: before add _all__ in sound/__init__.py
➜  /tmp python
Python 2.7.12 (default, Nov 20 2017, 18:23:56)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from sound import *
>>> dir()
['__builtins__', '__doc__', '__name__', '__package__']

# __all__: after add __all__ in sound/__init__.py
➜  /tmp python
Python 2.7.12 (default, Nov 20 2017, 18:23:56)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from sound import *
>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'fuzz', 'utils']

# __path__: before add __path__ in sound/utils/__init__.py
>>> import sound.utils.echo
This is normal echo

# __path__: after add __path__ in sound/utils/__init__.py
➜  /tmp python
Python 2.7.12 (default, Nov 20 2017, 18:23:56)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import sound.utils.echo
sound.utils.__init__.__path__ before change: ['sound/utils']
sound.utils.__init__.__path__ after change: ['sound/utils/linux', 'sound/utils']
This is linux echo

# __path__: the code in sound/utils/__init__.py
import os
import sys

print('sound.utils.__init__.__path__ before change: {}'.format(__path__))
dirname = __path__[0]

if sys.platform[0:5] == 'linux':
    __path__.insert(0, os.path.join(dirname, 'linux'))
else:
    __path__.insert(0, os.path.join(dirname, 'windows'))

print('sound.utils.__init__.__path__ after change: {}'.format(__path__))
```

### 静态方法和类方法


```python
class User(object):
    a = 1
    @staticmethod
    def b():
        print(self.a)
    @classmethod
    def c(cls):
        print(cls.a)
        
u = User()
```


```python
u.b()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-2-9bd563bff4c0> in <module>()
    ----> 1 u.b()
    

    <ipython-input-1-507161e2fc59> in b()
          3     @staticmethod
          4     def b():
    ----> 5         print(self.a)
          6     @classmethod
          7     def c(cls):


    NameError: global name 'self' is not defined



```python
User.b()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-3-f4347b1c4018> in <module>()
    ----> 1 User.b()
    

    <ipython-input-1-507161e2fc59> in b()
          3     @staticmethod
          4     def b():
    ----> 5         print(self.a)
          6     @classmethod
          7     def c(cls):


    NameError: global name 'self' is not defined



```python
u.c()
```

    1



```python
User.c()
```

    1



```python
class User(object):
    a = 1
    def b():
        print('1')
    def c(cls):
        print(cls.a)
        
u = User()
```


```python
u.c()
```

    1



```python
User.c()
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-11-9553038dc3d2> in <module>()
    ----> 1 User.c()
    

    TypeError: unbound method c() must be called with User instance as first argument (got nothing instead)



```python
u.b()
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-12-9bd563bff4c0> in <module>()
    ----> 1 u.b()
    

    TypeError: b() takes no arguments (1 given)



```python
User.b()
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-13-f4347b1c4018> in <module>()
    ----> 1 User.b()
    

    TypeError: unbound method b() must be called with User instance as first argument (got nothing instead)


### __slots__ 大量属性时减少内存占用


```python
class User(object):
    __slots__ = ('name', 'age')
    def __init__(self, name, age):
        self.name = name
        self.age = age
```


```python
u = User('Jason', 30)
```


```python
hasattr(u, '__dict__')
```




    False




```python
u.title = 'xxx'
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-17-f77daebddfb3> in <module>()
    ----> 1 u.title = 'xxx'
    

    AttributeError: 'User' object has no attribute 'title'


### 装饰器


```python
# 函数装饰器
def common(func):
    def _deco(*args, **kwargs):
        print('args:', args)
        return func(*args, **kwargs)
    return _deco
```


```python
@common
def test(p):
    print(p)
```


```python
test
```




    <function __main__._deco>




```python
test(1)
```

    ('args:', (1,))
    1



```python
# 类装饰器
class Common(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        print('args:', args)
        return self.func(*args, **kwargs)
```


```python
@Common
def test(p):
    print(p)
```


```python
test
```




    <__main__.Common at 0x5d1ccf8>




```python
test(1)
```

    ('args:', (1,))
    1



```python
# 给类的函数装饰器
def borg(cls):
    cls._state = {}
    orig_init = cls.__init__
    def new_init(self, *args, **kwargs):
        self.__dict__ = cls._state
        orig_init(self, *args, **kwargs)
    cls.__init__ = new_init
    return cls
```


```python
@borg
class A(object):
    def common(self):
        print(hex(id(self)))
```


```python
a, b = A(), A()
```


```python
b.d
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-35-5f3823c3dab6> in <module>()
    ----> 1 b.d
    

    AttributeError: 'A' object has no attribute 'd'



```python
a.d = 1
```


```python
b.d
```




    1




```python
# 带参数的装饰器
def common(*args, **kwargs):
    a = args
    def _common(func):
        def _deco(*args, **kwargs):
            print('args:', args, a)
            return func(*args, **kwargs)
        return _deco
    return _common
```


```python
@common('c')
def test(p):
    print(p)
```


```python
test
```




    <function __main__._deco>




```python
test(1)
```

    ('args:', (1,), ('c',))
    1


### 描述符
1.当希望对某些类的属性进行特别的处理而不会对整体的其他属性有影响的话，可以使用描述符

2.只要一个类实现了__get__、__set__、__delete__方法就是描述符

3.描述符会“劫持”那些本对于self.__dict__的操作

4.把一个类的操作托付与另外一个类

5.静态方法，类方法，property都是构建描述符的方法（类）


```python
class C(object):
    def __init__(self):
        self._x = None
    def getx(self):
        print('get x')
        return self._x
    def setx(self, value):
        print('set x')
        self._x = value
    def delx(self):
        print('del x')
        del self._x
    x = property(getx, setx, delx, 'The x property')
```


```python
c = C()
c.x = 12
```

    set x



```python
c.x
```

    get x





    12




```python
class Parrot(object):
    def __init__(self):
        self._voltage = 100000
    @property
    def voltage(self):
        return self._voltage
    @voltage.setter
    def voltage(self, value):
        self._voltage = value
```


```python
c = Parrot()
```


```python
c.voltage
```




    100000




```python
c.voltage = 200
```


```python
c.voltage
```




    200




```python
a = 'a'
a.swapcase()
```




    'A'




```python
# 描述符的例子
class MyDescriptor(object):
    _value = ''
    def __get__(self, instance, klass):
        return self._value
    def __set__(self, instance, value):
        self._value = value.swapcase()

class Swap(object):
    swap = MyDescriptor()
```


```python
instance = Swap()
```


```python
instance.swap
```




    ''




```python
instance.swap = 'make it swap'
```


```python
instance.swap
```




    'MAKE IT SWAP'




```python
# __dict__被劫持了
instance.__dict__
```




    {}



Note:
* 所有Python函数都默认有一个描述符
* 这个描述符的特性在“类”这一个对象上下文之外没有任何意义
* 但只要到了类中，instance.swap变成了
```python
Swap.__dict__['swap'].__get__(instance, Swap)
```


```python
def t():
    pass
```


```python
dir(t)
```




    ['__call__',
     '__class__',
     '__closure__',
     '__code__',
     '__defaults__',
     '__delattr__',
     '__dict__',
     '__doc__',
     '__format__',
     '__get__',
     '__getattribute__',
     '__globals__',
     '__hash__',
     '__init__',
     '__module__',
     '__name__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     'func_closure',
     'func_code',
     'func_defaults',
     'func_dict',
     'func_doc',
     'func_globals',
     'func_name']




```python
# 用Python实现静态方法和类方法
class myStaticMethod(object):
    def __init__(self, method):
        self.staticmethod = method
    def __get__(self, object, type=None):
        return self.staticmethod

class myClassMethod(object):
    def __init__(self, method):
        self.classmethod = method
    def __get__(self, object, klass=None):
        if klass is None:
            klass = type(object)
        def newfunc(*args):
            return self.classmethod(klass, *args)
        return newfunc
```

### 元类
对象是类的实例，类是它的元类的实例


```python
class MyClass():
    pass
```


```python
type(MyClass)
```




    classobj




```python
class MyClass(object):
    pass
```


```python
type(MyClass)
```




    type




```python
type(type)
```




    type




```python
# 对于这个例子，有没有括号都无所谓
class MyClass:
    __metaclass__ = type
```


```python
type(MyClass)
```




    type




```python
print(MyClass)
```

    <class '__main__.MyClass'>



```python
print(MyClass())
```

    <__main__.MyClass object at 0x0000000005D3A208>


模拟生成一个类：下面的方式等同于：
```python
class Hello(object):
    def __init__(self, func):
        self.func = func
     def hello(self):
        print('hello world')
```


```python
# 模拟生成一个类
def __init__(self, func):
    self.func = func

def hello(self):
    print('hello world')

attrs = {'__init__': __init__, 'hello': hello}
bases = (object,)
Hello = type('Hello', bases, attrs)
```


```python
h = Hello(lambda a, b=3: a + b)
```


```python
h.func(1, 3)
```




    4




```python
h.hello()
```

    hello world



```python
# 实现一个元类
class HelloMeta(type):
    def __new__(cls, name, bases, attrs):
        def __init__(cls, func):
            cls.func = func
        def hello(cls):
            print('hello world')
        t = type.__new__(cls, name, bases, attrs)
        t.__init__ = __init__
        t.hello = hello
        # Return创建的类
        return t
```


```python
class NewHello(object):
    __metaclass__ = HelloMeta
```


```python
nh = NewHello(lambda a: a + 1)
```


```python
nh.hello()
```

    hello world



```python
# 难懂的元类
hellometa = lambda name, parents, attrs: type(
    name,
    parents,
    dict(attrs.items() + [
        ('__new__', classmethod(
        lambda cls, *args, **kwargs:
            super(type(cls), cls).__new__(
                *args, **kwargs)
        )),
        ('hello', hello),
        ('__init__', __init__)
    ])
)
```


```python
class NewHello2(object):
    __metaclass__ = hellometa
```


```python
h = NewHello2(lambda x: x)
```

    c:\python27\lib\site-packages\ipykernel_launcher.py:9: DeprecationWarning: object() takes no parameters
      if __name__ == '__main__':



```python
h.func
```




    <function __main__.<lambda>>



### 模块：itertools（一）


```python
import itertools
```


```python
l = [(1, 10), (2, 10), (3, 20), (4, 20)]
```


```python
for key, group in itertools.groupby(l, lambda t: t[1]):
    print(key, list(group))
```

    (10, [(1, 10), (2, 10)])
    (20, [(3, 20), (4, 20)])



```python
# Referer for enumerate: http://www.runoob.com/python/python-func-enumerate.html
list(enumerate(range(10)))
```




    [(0, 0),
     (1, 1),
     (2, 2),
     (3, 3),
     (4, 4),
     (5, 5),
     (6, 6),
     (7, 7),
     (8, 8),
     (9, 9)]




```python
# Referer for izip_longest: https://blog.csdn.net/orangleliu/article/details/23737701
def chunker(items, chunk_size):
    args = [iter(items)] * chunk_size
    return itertools.izip_longest(*args)
```


```python
# Referer for filter: http://w ww.runoob.com/python/python-func-filter.html
for i in chunker(range(10), 4):
    print(filter(lambda x:x is not None, list(i)))
```

    [0, 1, 2, 3]
    [4, 5, 6, 7]
    [8, 9]


### 模块：collections（二）


```python
import collections
```


```python
words = 'Python is a good thing, not a bad thing'
words = words.replace(',', '').split(' ')
```


```python
collections.Counter(words).most_common(10)
```




    [('a', 2),
     ('thing', 2),
     ('good', 1),
     ('Python', 1),
     ('is', 1),
     ('bad', 1),
     ('not', 1)]




```python
Q = collections.deque()
```


```python
Q.append(1)
```


```python
Q.appendleft(2)
```


```python
Q
```




    deque([2, 1])




```python
Q.extend([3, 4])
```


```python
Q
```




    deque([2, 1, 3, 4])




```python
Q.extendleft([5, 6])
```


```python
Q
```




    deque([6, 5, 2, 1, 3, 4])




```python
Q.pop()
```




    4




```python
Q.popleft()
```




    6




```python
Q
```




    deque([5, 2, 1, 3])




```python
Q.rotate(3)
```


```python
Q
```




    deque([2, 1, 3, 5])




```python
m = dict((str(x), x) for x in range(10))
```


```python
print(','.join(m.keys()))
```

    1,0,3,2,5,4,7,6,9,8



```python
m = collections.OrderedDict((str(x), x) for x in range(10))
```


```python
m
```




    OrderedDict([('0', 0),
                 ('1', 1),
                 ('2', 2),
                 ('3', 3),
                 ('4', 4),
                 ('5', 5),
                 ('6', 6),
                 ('7', 7),
                 ('8', 8),
                 ('9', 9)])




```python
d = {}
```


```python
for k, v in [('a', 1), ('c', 2), ('a', 3)]:
    if k in d:
        d[k] += v
    else:
        d[k] = v
```


```python
d
```




    {'a': 4, 'c': 2}




```python
m = collections.defaultdict(int)
```


```python
m['a']
```




    0




```python
for k, v in [('a', 1), ('c', 2), ('a', 3)]:
    m[k] += v
```


```python
m
```




    defaultdict(int, {'a': 4, 'c': 2})




```python
# 默认值为1的dict
g = collections.defaultdict(lambda: 1)
```


```python
g['a'] += 1
```


```python
g
```




    defaultdict(<function __main__.<lambda>>, {'a': 2})




```python
g['b']
```




    1



### operator模块（一）


```python
import operator
```


```python
reduce(+, (5, 4, 3, 2, 1))
```


      File "<ipython-input-209-7006c100d9dc>", line 1
        reduce(+, (5, 4, 3, 2, 1))
                ^
    SyntaxError: invalid syntax




```python
reduce(operator.add, (5, 4, 3, 2, 1))
```




    15




```python
l = [1, 2, 3, 4, 5]
```


```python
operator.itemgetter(1)(l)
```




    2




```python
operator.itemgetter(1, 3, 4)(l)
```




    (2, 4, 5)




```python
inventory = [('apple', 3), ('banana', 2), ('pear', 5), ('orange', 1)]
```


```python
sorted(inventory, key=operator.itemgetter(1))
```




    [('orange', 1), ('banana', 2), ('apple', 3), ('pear', 5)]




```python
class fclass(object):
    def test(self, param):
        print(param)
```


```python
fc = fclass()
```


```python
# 等同于fc.test(1)
operator.methodcaller('test', '1')(fc)
```

    1



```python
import sys
```


```python
operator.attrgetter('platform')(sys)
```




    'win32'



### functools模块
functools.partial冻结部分函数位置参数或关键字参数，简化函数


```python
import functools
```


```python
def test(a, b):
    print(a, b)
```


```python
p_test = functools.partial(test, a=10)
```


```python
p_test(b=10)
```

    (10, 10)


wraps把被封装函数的name，module，doc和dict都复制到封装函数中
partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)的简写


```python
def common(func):
    def _deco(*args, **kwargs):
        '''In _deco'''
        return func(*args, **kwargs)
    return _deco
```


```python
@common
def test(p):
    '''In test'''
    print(p)
```


```python
test.__doc__
```




    'In _deco'




```python
def common(func):
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        '''In _deco'''
        return func(*args, **kwargs)
    return _deco
```


```python
test.__doc__
```




    'In test'



functools.cmp_to_key将老式比较函数转换成key函数，用在接受key函数的比较方法中


```python
def mycmp(x, y):
    x, y = int(x), int(y)
    return (x > y) - (x < y)
```


```python
1 > 2 - 1 < 2
```




    False




```python
values = [5, '3', 7]
```


```python
sorted(values, key=functools.cmp_to_key(mycmp))
```




    ['3', 5, 7]



functools.total_ordering，比较判定


```python
@functools.total_ordering
class Test:
    def __init__(self, value):
        self.value = value
    def __lt__(self, other):
        return self.value < other.value
```


```python
# No __eq__ generated
vars(Test)
```




    {'__doc__': None,
     '__ge__': <function functools.__ge__>,
     '__gt__': <function functools.__gt__>,
     '__init__': <function __main__.__init__>,
     '__le__': <function functools.__le__>,
     '__lt__': <function __main__.__lt__>,
     '__module__': '__main__'}




```python
Test(1) < Test(2)
```




    True




```python
Test(3) > Test(2)
```




    True




```python
Test(2) <= Test(2)
```




    False




```python
@functools.total_ordering
class Test:
    def __init__(self, value):
        self.value = value
    def __lt__(self, other):
        return self.value < other.value
    def __eq__(self, other):
        return self.value == other.value
```


```python
Test(2) <= Test(2)
```




    True



### 开发中遇到的问题

可变默认参数


```python
def append_to(element, to=[]):
    to.append(element)
    return to
```


```python
my_list = append_to(12)
```


```python
my_list
```




    [12]




```python
other_list = append_to(21)
```


```python
other_list
```




    [12, 21]




```python
id(my_list)
```




    98088264L




```python
id(other_list)
```




    98088264L



闭包变量绑定


```python
def create_multipliers():
    return [lambda x: i * x for i in range(5)]
```


```python
items = create_multipliers()
```


```python
items
```




    [<function __main__.<lambda>>,
     <function __main__.<lambda>>,
     <function __main__.<lambda>>,
     <function __main__.<lambda>>,
     <function __main__.<lambda>>]




```python
for item in items:
    print(item(2))
```

    8
    8
    8
    8
    8



```python
def create_multipliers():
    s = [lambda x: i * x for i in range(5)]
    print(locals()['i'])
    return s
```


```python
items = create_multipliers()
```

    4



```python
def create_multipliers():
    return [lambda x, i=i: i * x for i in range(5)]
```


```python
items = create_multipliers()
```


```python
for item in items:
    print(item(2))
```

    0
    2
    4
    6
    8


或者


```python
from functools import partial
from operator import mul
```


```python
def create_multipliers():
    return [partial(mul, i) for i in range(5)]
```


```python
items = create_multipliers()
```


```python
for item in items:
    print(item(2))
```

    0
    2
    4
    6
    8

