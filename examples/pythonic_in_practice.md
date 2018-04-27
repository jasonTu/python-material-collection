
## Pthonic Code in Practice
此文章收集平时工作中一些Pythonic code，以供后面参考。

### 循环结束处理
通常以往的做法是设置一个标志位来处理或其他额外处理:
```python
def get_file_content(fpath):
    """Get file content by the right encoding."""
    G_ENCODING_LIST = ['utf-8', 'gbk', 'latin1']
    for encode in G_ENCODING_LIST:
        try:
            content = open(fpath, encoding=encode).read()
            return content
        except UnicodeDecodeError:
            if encode == G_ENCODING_LIST[-1]:
                raise
        except FileNotFoundError:
            raise
```
    
而下例中的做法则是利用了Python本身语法的特性：

```python
def get_file_content(fpath):
    """Get file content by the right encoding."""
    G_ENCODING_LIST = ['utf-8', 'gbk', 'latin1']
    for encode in G_ENCODING_LIST:
        try:
            content = open(fpath, encoding=encode).read()
            return content
        except UnicodeDecodeError:
            pass
        except FileNotFoundError:
            raise
    else:
        raise UnicodeDecodeError
```

另外需要注意的是:
* 在except分支中，如果是抛出刚抓取的异常，可不必指定。
* 为了避免过深的try except嵌套，这里使用了for循环使代码块更加扁平

### 列表生成式
创建列表，通常的做法可以是这样：

```python
def add_patterns(self, ptn_docs):
    """Add pattern set info."""
    ltypes = []
    for ltype, doc in ptn_docs:
        ltypes.append(ltype)
        # 不使用列表表达式创建列表
        doc_list = []
        for word in jieba.cut(doc):
            doc_list.append(word)
        doc_list = [word for word in jieba.cut(doc)]
        doc_list = list(set(doc_list) - set(G_STOP_WORDS))
        self._ptn_simtest_dbs[ltype]['all_doc_list'].append(doc_list)
        self._ptn_simtest_dbs[ltype]['dict'].add_documents([doc_list])
    ......
```

Pythonic的做法则是这样：

```python
def add_patterns(self, ptn_docs):
    """Add pattern set info."""
    ltypes = []
    for ltype, doc in ptn_docs:
        ltypes.append(ltype)
        # 使用列表表达式创建列表
        doc_list = [word for word in jieba.cut(doc)]
        doc_list = list(set(doc_list) - set(G_STOP_WORDS))
        self._ptn_simtest_dbs[ltype]['all_doc_list'].append(doc_list)
        self._ptn_simtest_dbs[ltype]['dict'].add_documents([doc_list])
    ......
```

注释：
* 这里使用了集合差的方式求列表差集：
```python
doc_list = list(set(doc_list) - set(G_STOP_WORDS))
```

### 布尔值判断
根据判断对象结果返回True or False，可以通过以下方法简写：

```python
def _check_fingerprint(self, suspect):
    """Check whether fingerprint exist."""
    content = open(suspect, 'rb').read()
    md5sum = hashlib.md5(content).hexdigest()
    wsp = self.ws_data.filter(fingerprint=md5sum)
    return True is wsp else False
```

还有更简洁的写法吗：

```python
def _check_fingerprint(self, suspect):
    """Check whether fingerprint exist."""
    content = open(suspect, 'rb').read()
    md5sum = hashlib.md5(content).hexdigest()
    wsp = self.ws_data.filter(fingerprint=md5sum)
    return bool(wsp)
```

### goto in Python
记得学习C语言的时候，老师通常会说不建议我们使用“goto”这样的语法，以免造成意想不到的结果。
但实际工作中，想“goto”这种语法糖在有些场景中有让人爱不释手。

先看这个场景，下面代码解析一个压缩包中的pattern是否满足指定格式：

```python
def check_pattern_package(fpath):
    """Check pattern package correctness."""
    base_dir = os.path.dirname(fpath)
    ret, reason, extract_dir = True, None, None
    with zipfile.ZipFile(fpath) as zf:
        infolist = zf.infolist()
        if not infolist[0].is_dir():
            return False, REST_ERR_400_ZIP_BADFILE
        zf_base_dir = infolist[0].filename
        md5sum_file = os.path.join(zf_base_dir, 'md5sum.txt')
        if md5sum_file not in zf.namelist():
            return False, REST_ERR_400_ZIP_BADFORMAT
        zf.extractall(base_dir)

    extract_dir = os.path.join(base_dir, zf_base_dir)
    try:
        with open(os.path.jion(base_dir, md5sum_file)) as md5_fp:
            reader = csv.reader(md5_fp, delimiter=' ')
    except FileNotFoundError:
        return False, REST_ERR_400_ZIP_BADFORMAT
    else:
        for row in reader:
            if len(row) < 2:
                raise PtnPackageParseError(REST_ERR_400_ZIP_BADFORMAT)
            pzf = os.path.join(extract_dir, row[1])
            with open(pzf, 'rb') as fpzf:
                fdata = fpzf.read()
            md5sum = hashlib.md5(fdata).hexdigest()
            if md5sum != row[0]:
                return False, REST_ERR_400_ZIP_BADFILE
    return True, _
```

在上述代码中，为了更好的执行效率，一旦发现格式不符函数直接返回。

现在对这个函数有一个新的需求：根据函数的输入参数，删除压缩包和解压缩目录所有文件。对于该需求，如果按照上述代码执行，则需要在每一个“return”关键字处对需要删除的文件进行处理，这样会有很多重复代码。以往在C语言中，使用“goto”可以很好的完成任务，很遗憾Python并不支持“goto”。

使用“try exception”控制代码执行路径模拟“goto”:

```python
class PtnPackageParseError(Exception):

    """Exception for pattern package parse."""

    def __init__(self, reason, message=''):
        self.reason = reason
        self.message = message
        super().__init__()
        
        
def check_pattern_package(fpath, cleanup=False):
    """Check pattern package correctness."""
    base_dir = os.path.dirname(fpath)
    ret, reason, extract_dir = True, None, None
    try:
        with zipfile.ZipFile(fpath) as zf:
            infolist = zf.infolist()
            if not infolist[0].is_dir():
                raise PtnPackageParseError(REST_ERR_400_ZIP_BADFILE)
            zf_base_dir = infolist[0].filename
            md5sum_file = os.path.join(zf_base_dir, 'md5sum.txt')
            if md5sum_file not in zf.namelist():
                raise PtnPackageParseError(REST_ERR_400_ZIP_BADFORMAT)
            zf.extractall(base_dir)

        extract_dir = os.path.join(base_dir, zf_base_dir)
        try:
            with open(os.path.jion(base_dir, md5sum_file)) as md5_fp:
                reader = csv.reader(md5_fp, delimiter=' ')
        except FileNotFoundError:
            raise PtnPackageParseError(REST_ERR_400_ZIP_BADFORMAT)
        else:
            for row in reader:
                if len(row) < 2:
                    raise PtnPackageParseError(REST_ERR_400_ZIP_BADFORMAT)
                pzf = os.path.join(extract_dir, row[1])
                with open(pzf, 'rb') as fpzf:
                    fdata = fpzf.read()
                md5sum = hashlib.md5(fdata).hexdigest()
                if md5sum != row[0]:
                    raise PtnPackageParseError(REST_ERR_400_ZIP_BADFILE)
    except PtnPackageParseError as e:
        ret, reason = False, e.reason
    finally:
        if cleanup:
            os.unlink(fpath)
            if os.path.exists(extract_dir):
                os.removedirs(extract_dir)
    return ret, reason, extract_dir
```
