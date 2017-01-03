## Meta Class Example in ORM
```python
# coding: utf-8

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = {}
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print('Found mapping: %s==>%s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__table__'] = name
        attrs['__mappings__'] = mappings
        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute %s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (
            self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))


class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()

"""
Result:
[root@localhost py]# python meta_example.py
Found mapping: email==><StringField:email>
Found mapping: password==><StringField:password>
Found mapping: id==><IntegerField:id>
Found mapping: name==><StringField:username>
SQL: insert into User (password,email,username,id) values (?,?,?,?)
ARGS: ['my-pwd', 'test@orm.org', 'Michael', 12345]
"""
```

## Magic Method Signatures
```python
# coding: utf-8

class Meta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        print(' Meta.__prepare__(mcs=%s, name=%r, bases=%s, **%s' % (
            mcs, name, bases, kwargs
        ))
        return {}

    def __new__(mcs, name, bases, attrs, **kwargs):
        print(' Meta.__new__(mcs=%s, name=%r, bases=%s, attrs=[%s], **%s' % (
            mcs, name, bases, ', '.join(attrs), kwargs
        ))
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, **kwargs):
        print(' Meta.__init__(mcs=%s, name=%r, bases=%s, attrs=[%s], **%s' % (
            cls, name, bases, ', '.join(attrs), kwargs
        ))
        return super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        print(' Meta.__call__(cls=%s, args=%s, kwargs=%s' % (
            cls, args, kwargs
        ))
        return super().__call__(*args, **kwargs)


class Class(metaclass=Meta, extra=1):
    def __new__(cls, myarg):
        print(' Class.__new__(cls=%s, myarg=%s)' % (
            cls, myarg
        ))
        return super().__new__(cls)

    def __init__(self, myarg):
        print(' Class.__init__(self=%s, myarg=%s)' % (
            self, myarg
        ))
        self.myarg = myarg
        return super().__init__()

    def __str__(self):
        return '<instance of Class; myargs=%s>' % (
            getattr(self, 'myarg', 'MISSING'),
        )
```
