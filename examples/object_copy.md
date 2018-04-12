
## Python对象的浅拷贝和深拷贝
Python中的赋值语句不会创建对象的副本，而只是给独享绑定了新的名称。


```python
obj = 1
obj2 = obj
```


```python
obj is obj2
```




    True




```python
id(obj)
```




    31034104L




```python
id(obj2)
```




    31034104L



我们看看如何拷贝Python的内置集合。通过在现在集合上调用其工厂函数即可拷贝Python的内置可变集合（如列表，字典和集合）：


```python
orig_list = [1, 2, 3]
orig_dict = {'name': 'Jason'}
orig_set = set(orig_list)
new_list = list(orig_list)
new_dict = dict(orig_dict)
new_set = set(orig_set)
```

但是此方法不适用自定义对象，并且最重要的是，它仅创建浅拷贝。对于像列表，字典和集合这样的复合对象，浅拷贝和深拷贝之间有一个重要区别：
* 浅拷贝值构建一个新的集合独享，然后用原对象的子对象的引用填充它。实质上，浅拷贝只有一层。拷贝不会递归，因此不会创建对象本身的副本
* 深拷贝会递归拷贝。这意味着会首先构造一个新的集合对象，然后递归地填充原始对象中的子对象的副本。以这种方式拷贝对象会遍历整个对象树，从而创建原始对象及其所有子对象的完全独立的副本


```python
new_list is orig_list
```




    False




```python
new_dict is orig_dict
```




    False




```python
new_set is orig_set
```




    False



### 创建浅拷贝
在下面的额例子中，我们将创建一个新的嵌套列表，然后用工厂函数对它进行浅拷贝


```python
xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
ys = list(xs)
```


```python
xs
```




    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]




```python
ys
```




    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]




```python
xs is ys
```




    False




```python
xs.append([10, 11, 12])
```


```python
xs
```




    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]




```python
ys
```




    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]




```python
ys[0][0] = 'a'
```


```python
ys
```




    [['a', 2, 3], [4, 5, 6], [7, 8, 9]]




```python
xs
```




    [['a', 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]



现在了解了如何创建一些内置集合类的浅拷贝，并且也知道了浅拷贝和深拷贝之间的区别，那么现在的问题是：
* 如何创建内置集合的深拷贝
* 如何创建任意对象的（浅和深）拷贝，包括自定义类

### 创建深拷贝
上诉问题的答案是使用Python标准库中的copy模块，该模块提供了一个简单的接口来创建任意Python对象的深浅拷贝。


```python
import copy
xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
zs = copy.deepcopy(xs)
```


```python
xs is zs
```




    False




```python
zs[0][0] = 'a'
```


```python
zs
```




    [['a', 2, 3], [4, 5, 6], [7, 8, 9]]




```python
xs
```




    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]




```python
xs.append([10, 11, 12])
```


```python
zs
```




    [['a', 2, 3], [4, 5, 6], [7, 8, 9]]



当然，你也可以通过copy模块中的函数创建浅拷贝，copy.copy()函数会创建对象的浅拷贝。


```python
xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
zs = copy.copy(xs)
```


```python
xs is zs
```




    False




```python
xs.append([10, 11, 12])
```


```python
xs
```




    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]




```python
zs
```




    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]




```python
xs[0][0] = 'a'
```


```python
xs
```




    [['a', 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]




```python
zs
```




    [['a', 2, 3], [4, 5, 6], [7, 8, 9]]



### 复制任意Python对象
copy模块不仅能复制内置对象外，它可以复制任何对象。


```python
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'Point(%r, %r)' % (self.x, self.y)
```

对象浅拷贝：


```python
a = Point([1, 2, 3], [4, 5, 6])
b = copy.copy(a)
```


```python
a
```




    Point([1, 2, 3], [4, 5, 6])




```python
b
```




    Point([1, 2, 3], [4, 5, 6])




```python
a.x[0] = 0
```


```python
a
```




    Point([0, 2, 3], [4, 5, 6])




```python
b
```




    Point([0, 2, 3], [4, 5, 6])



对象深拷贝：


```python
c = Point([1, 2, 3], [4, 5, 6])
d = copy.deepcopy(c)
```


```python
c
```




    Point([1, 2, 3], [4, 5, 6])




```python
d
```




    Point([1, 2, 3], [4, 5, 6])




```python
c.x[0] = 4
```


```python
c
```




    Point([4, 2, 3], [4, 5, 6])




```python
d
```




    Point([1, 2, 3], [4, 5, 6])



### 小结
* 创建对象的浅拷贝不会克隆子对象，因此副本不完全独立于原对象
* 对象的深层副本将递归地拷贝子对象，拷贝完全独立于原始文件，但创建深拷贝较慢
* 可以使用copy模块拷贝任何对象（包括内置对象和自定义类）
