
# Python对象序列化和反序列化
通过将对象序列化可以将其存储在变量或者文件中，可以保存当时对象的状态，实现其生命周期的延长。并且需要时可以再次将这个对象读取出来。Python中有几个常用模块可实现这一功能。

## Pickle模块


```python
import pickle
```

### 存储在变量中


```python
dic = {'age': 23, 'job': 'engineer'}
byte_data = pickle.dumps(dic)
print(byte_data)
```

    b'\x80\x03}q\x00(X\x03\x00\x00\x00jobq\x01X\x08\x00\x00\x00engineerq\x02X\x03\x00\x00\x00ageq\x03K\x17u.'



```python
obj = pickle.loads(byte_data)
print(obj)
```

    {'job': 'engineer', 'age': 23}


### 存储到文件中


```python
with open('object_serializer/sample.pkl', 'wb') as fp:
    pickle.dump(dic, fp)
```


```python
with open('object_serializer/sample.pkl', 'rb') as fp:
    obj = pickle.load(fp)
    print(obj)
    print(type(obj))
```

    {'job': 'engineer', 'age': 23}
    <class 'dict'>


### 序列化自定义对象和类


```python
class Person:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job
    
    def work(self):
        print(self.name, 'is working...')
```


```python
per = Person('Jason', 25, 'engineer')
pkl_data = pickle.dumps(per)
print(pkl_data)
ld_per = pickle.loads(pkl_data)
print(ld_per)
```

    b'\x80\x03c__main__\nPerson\nq\x00)\x81q\x01}q\x02(X\x04\x00\x00\x00nameq\x03X\x05\x00\x00\x00Jasonq\x04X\x03\x00\x00\x00ageq\x05K\x19X\x03\x00\x00\x00jobq\x06X\x08\x00\x00\x00engineerq\x07ub.'
    <__main__.Person object at 0x7f38b414e048>



```python
ld_per.name
```




    'Jason'




```python
pkl_cls_per = pickle.dumps(Person)
LdPerson = pickle.loads(pkl_cls_per)
p = LdPerson('Jammy', 5, 'Child')
```


```python
type(p)
```




    __main__.Person




```python
p.name
```




    'Jammy'



## json模块
pickle可以很方便地序列化所有对象。不过json作为更为标准的格式，具有更好的可读性（pickle是二进制数据）和跨平台性。是个不错的选择。

json使用的四个函数名和pickle一致。


```python
import json
```


```python
def person2dict(person):
    return {
        'name': person.name,
        'age': person.age,
        'job': person.job
    }

def dict2person(dic):
    return Person(dic['name'], dic['age'], dic['job'])
```


```python
per = Person('Jason', 25, 'engineer')
# 此处需要一个转换函数
data_per = json.dumps(per, default=person2dict)
```


```python
data_per
```




    '{"job": "engineer", "name": "Jason", "age": 25}'




```python
ld_per = json.loads(data_per, object_hook=dict2person)
```


```python
ld_per
```




    <__main__.Person at 0x7f38b4140eb8>




```python
ld_per.name
```




    'Jason'


