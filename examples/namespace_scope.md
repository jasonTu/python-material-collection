
# Namespace and Scope（命名空间和作用域）:Python2.x

## namespace

Namespace（只）是 从名字到对象的一个映射(a mapping from name to objects) 。大部分namespace都是按Python中的字典来实现的。有一些常见的namespace：built-in中的集合（ abs() 函数等）、一个模块中的全局变量等。

从某种意义上来说，一个对象(object)的所有属性(attribute)也构成了一个namespace。在程序执行期间，可能（其实是肯定）会有多个名空间同时存在。不同namespace的创建/销毁时间也不同。

此外，两个不同namespace中的两个相同名字的变量之间没有任何联系。

## scope

有了namespace基础之后，让我们再来看看scope。Scope是Python程序的一块文本区域(textual region)。

在该文本区域中，对namespace是可以直接访问，而不需要通过属性来访问。

Scope是定义程序该如何搜索确切地“名字-对象”的名空间的层级关系。
(The “scope” in Python defines the “hirerchy level” in which we search namespaces for
certain “name-to-object” mappings.)

Tip

直接访问：对一个变量名的引用会在所有namespace中查找该变量，而不是通过属性访问。

属性访问：所有名字后加 . 的都认为是属性访问。

如 module_name.func_name ，需要指定 func_name 的名空间，属于属性访问。
而 abs(-1) ， abs 属于直接访问。

## 两者之间有什么联系呢？

Important

在Python中，scope是由namespace按特定的层级结构组合起来的。

scope一定是namespace，但namespace不一定是scope.

## LEGB-rule

在一个Python程序运行中，至少有4个scopes是存在的。

直接访问一个变量可能在这四个namespace中逐一搜索。
* Local(innermost)
包含局部变量。
比如一个函数/方法内部。
* Enclosing
包含了非局部(non-local)也非全局(non-global)的变量。
比如两个嵌套函数，内层函数可能搜索外层函数的namespace，但该namespace对内层函数而言既非局部也非全局。 
* Global(next-to-last)
当前脚本的最外层。
比如当前模块的全局变量。 
* Built-in(outtermost)
Python __builtin__ 模块。
包含了内建的变量/关键字等。 
那么，这么多的作用域，Python是按什么顺序搜索对应作用域的呢？

著名的”LEGB-rule”，即scope的搜索顺序：

Important

Local -> Enclosing -> Global -> Built-in

怎么个意思呢？

当有一个变量在 local 域中找不到时，Python会找上一层的作用域，即 enclosing 域（该域不一定存在）。enclosing 域还找不到的时候，再往上一层，搜索模块内的 global 域。最后，会在 built-in 域中搜索。对于最终没有搜索到时，Python会抛出一个 NameError 异常。

作用域可以嵌套。比如模块导入时。

这也是为什么不推荐使用 from a_module import * 的原因，导入的变量可能被当前模块覆盖。


```python
# Assignment rule
```


```python
def outer():
    a = 0
    b = 1
    def inner():
        print(a)
        print(b)
        
    inner()

outer()
```

    0
    1



```python
# Add one expression then
```


```python
def outer():
    a = 0
    b = 1
    def inner():
        print(a)
        # 当解释器执行到这里时，发现变量b目前还没有找到，会继续尝试把整块代码解释完，，然后发现找到了b的定义
        # 然而在b赋值之前，先打印会导致报错
        print(b)
        
        b = 4
    
    inner()
    
outer()
```

    0



    ---------------------------------------------------------------------------

    UnboundLocalError                         Traceback (most recent call last)

    <ipython-input-8-85c08ac56cd6> in <module>()
         12     inner()
         13 
    ---> 14 outer()
    

    <ipython-input-8-85c08ac56cd6> in outer()
         10         b = 4
         11 
    ---> 12     inner()
         13 
         14 outer()


    <ipython-input-8-85c08ac56cd6> in inner()
          6         # 当解释器执行到这里时，发现变量b目前还没有找到，会继续尝试把整块代码解释完，，然后发现找到了b的定义
          7         # 然而在b赋值之前，先打印会导致报错
    ----> 8         print(b)
          9 
         10         b = 4


    UnboundLocalError: local variable 'b' referenced before assignment


在这个例子中，只有A语句没有B语句也会导致同样的结果。
因为 b += 1 等同于 b = b + 1。

对于变量的作用域查找有了了解之后，还有两条很重要的规则：

Important

* 赋值语句通常隐式地会创建一个局部(local)变量，即便该变量名已存在于赋值语句发生的上一层作用域中；
* 如果没有 global 关键字声明变量，对一个变量的赋值总是认为该变量存在于最内层(innermost)的作用域中；

也就是说在作用域内有没有发生赋值是不一样的。

但是，在这点上，Python 2和Python 3又有不同， [Python access non-local variable](http://stackoverflow.com/questions/13282910/python-cant-access-nonlocal-variable-before-local-variable-is-defined-with-same):

Python’s scoping rules indicate that a function defines a new scope level,
and a name is bound to a value in only one scope level – it is statically scoped.

…

In Python 2.x, it is not possible to modify a non-local variable;
* you have either read-only access to a global or non-local variable,
* or read-write access to a global variable by using the global statement,
* or read-write access to a local variable (by default).

In Python 3.x, the nonlocal statement has been introduced with a similar effect
to global, but for an intermediate scope.


```python
def outer():
    a = 0
    b = 1
    def inner():
        print(a)
        # 当解释器执行到这里时，发现变量b目前还没有找到，会继续尝试把整块代码解释完，，然后发现找到了b的定义
        # 然而在b赋值之前，先打印会导致报错
        print(b)
        
        b += 1
    
    inner()
    
outer()
```

    0



    ---------------------------------------------------------------------------

    UnboundLocalError                         Traceback (most recent call last)

    <ipython-input-9-3e3c644d266a> in <module>()
         12     inner()
         13 
    ---> 14 outer()
    

    <ipython-input-9-3e3c644d266a> in outer()
         10         b += 1
         11 
    ---> 12     inner()
         13 
         14 outer()


    <ipython-input-9-3e3c644d266a> in inner()
          6         # 当解释器执行到这里时，发现变量b目前还没有找到，会继续尝试把整块代码解释完，，然后发现找到了b的定义
          7         # 然而在b赋值之前，先打印会导致报错
    ----> 8         print(b)
          9 
         10         b += 1


    UnboundLocalError: local variable 'b' referenced before assignment


## for循环


```python
for i in xrange(10):
    print(i)
print(i)
```

    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    9


有点不可思议是不是？

在 [Python 2.x for语句](https://docs.python.org/2.7/reference/compound_stmts.html#the-for-statement) 中是这么说的：

The for-loop makes assignments to the variable(s) in the target list.
This overwrites all previous assignments to those variablees including those made in the suite of the for-loop.

…

The target list is not deleted when the loop is finished.
But if the sequence is empty, they will not have been assigned to at all the loop.

for 后面跟着的变量(target list)在循环结束后是不会被删除的，
但如果 for 循环的序列为空，这些变量是完全不会被赋值的。

这在Python中是个大坑啊。

避免这个坑的解决办法就是规范命名规范。
比如用于循环的变量尽量使用单字符。在任何有疑议的情况可以直接将索引值初始化。

## List Comprehension vs. Generator Expression
* 列表推导式(List Comprehension): [expression for var in iterable]
* 生成器表达式(Generator Expression): (expression for var in iterable)


```python
class A(object):
    a = 3
    b = list((a + i for i in xrange(10)))
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-18-1d8243f27b6c> in <module>()
    ----> 1 class A(object):
          2     a = 3
          3     b = list((a + i for i in xrange(10)))


    <ipython-input-18-1d8243f27b6c> in A()
          1 class A(object):
          2     a = 3
    ----> 3     b = list((a + i for i in xrange(10)))
    

    <ipython-input-18-1d8243f27b6c> in <genexpr>((i,))
          1 class A(object):
          2     a = 3
    ----> 3     b = list((a + i for i in xrange(10)))
    

    NameError: global name 'a' is not defined


class没有作用域(scope)，但有一个局部的名空间(namespace)，它并不构成一个作用域。
这意味着在类定义中的表达式可以访问该名空间。

但在类体(class body)中， 对 b 的赋值表达式中，该表达式引入了一个新的作用域，该作用域并不能访问类的名空间。

就像刚刚说的，函数会引入一个新的作用域。


```python
class A(object):
    a = 3
    # Python2中，列表推导式没有生成新的作用域
    b = list([a + i for i in xrange(10)])
```

而对于Python 2和Python 3，生成器表达式都有引入新的作用域。


```python
# 附一份：访问权限汇总表
import pandas
data = pandas.DataFrame({
    'Can Access class attributes': ['list comp. iterable', 'list comp. expression', 'gen expr. iterable', 'gen expr. expression	', 'dict comp. iterable', 'dict comp expression'],
    'Python 2': list('YYYNYN'),
    'Python 3': list("YNYNYN")
})
```


```python
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Can Access class attributes</th>
      <th>Python 2</th>
      <th>Python 3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>list comp. iterable</td>
      <td>Y</td>
      <td>Y</td>
    </tr>
    <tr>
      <th>1</th>
      <td>list comp. expression</td>
      <td>Y</td>
      <td>N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>gen expr. iterable</td>
      <td>Y</td>
      <td>Y</td>
    </tr>
    <tr>
      <th>3</th>
      <td>gen expr. expression\t</td>
      <td>N</td>
      <td>N</td>
    </tr>
    <tr>
      <th>4</th>
      <td>dict comp. iterable</td>
      <td>Y</td>
      <td>Y</td>
    </tr>
    <tr>
      <th>5</th>
      <td>dict comp expression</td>
      <td>N</td>
      <td>N</td>
    </tr>
  </tbody>
</table>
</div>



## 总结

本文介绍了Python中 namespace 和 scope 的区别，
以及复杂作用域的搜索规则（ LEGB ）。
此外，还介绍了一些常见的会创建scope的情况（函数定义，生成器表达式等），当然包括
了Python 2和Python 3中的不同实现。

Python中对于作用域的定义确实是个大问题，我并没有找到像 C 语言那样，
“代码块 {} 中定义的即是一个局部作用域”这样简洁的规则来清晰地表明
Python中作用域的 创建/销毁 的条件。

这篇文章的内容积压了很久，终于抽了点时间出来整理了下。

写的也有点没章法了，各位看官看得懂就看吧；看不懂多看几遍吧。

看望之后也提点啥建议意见之类的，好让后来人也能更快速简单的理解这个问题。
万一我理解错了呢？

欢迎探讨。

但有一点可以肯定，“这事儿还没完”。

## 参考文献

[1] [A Beginner Guide to Python’s namespaces and scope resolution](http://nbviewer.ipython.org/github/rasbt/python_reference/blob/master/tutorials/scope_resolution_legb_rule.ipynb)

[2] [Python Scopes and Namespaces](https://docs.python.org/2/tutorial/classes.html#python-scopes-and-namespaces)

[3] [Generator Expressions vs. List Comprehension](http://stackoverflow.com/questions/47789/generator-expressions-vs-list-comprehension)

[4] [Reference class variable in a comprehension of another class variable](http://stackoverflow.com/questions/11749629/reference-class-variable-in-a-comprehension-of-another-class-variable)

[5] [Undefined global in list generator expression](http://stackoverflow.com/questions/11669379/undefined-global-in-list-generator-expression-using-python3-works-with-python2/11670273)

[6] [Python access non-local variable](http://stackoverflow.com/questions/13282910/python-cant-access-nonlocal-variable-before-local-variable-is-defined-with-same)

[7] [Seeming unintended difference between list comprehensions and generator expressions](https://mail.python.org/pipermail/python-dev/2009-February/086287.html)

[8] [Python 2.x for语句](https://docs.python.org/2.7/reference/compound_stmts.html#the-for-statement)
