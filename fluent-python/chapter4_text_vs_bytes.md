
## Character Issues


```python
# Example 4-1 Encoding and decoding
s = 'caf艾'
len(s)
```




    4




```python
b = s.encode('utf-8')
b
```




    b'caf\xe8\x89\xbe'




```python
len(b)
```




    6




```python
b.decode('utf-8')
```




    'caf艾'



## Byte Essentials


```python
# Example 4-2
cafe = bytes('caf艾', encoding='utf8')
cafe
```




    b'caf\xe8\x89\xbe'




```python
# Each item is an integer in range(256)
cafe[0]
```




    99




```python
# Slices of bytes also bytes, even slices of a single byte
cafe[:1]
```




    b'c'




```python
cafe_arr = bytearray(cafe)
cafe_arr
```




    bytearray(b'caf\xe8\x89\xbe')




```python
# A slice of bytearray is also bytearray
cafe_arr[-1:]
```




    bytearray(b'\xbe')




```python
# Example 4-3 Initializing bytes from the raw data of an array
import array
numbers = array.array('h', [-2, -1, 0, 1, 2])
octers = bytes(numbers)
octers
```




    b'\xfe\xff\xff\xff\x00\x00\x01\x00\x02\x00'



## Structs and Memory Views


```python
# Example 4-4 Using memoryview and struct to inspect a GIF image header
import struct
# struct format: < little-endian; 3s3s two sequence of 3 bytes; HH two 16-bit integers
fmt = '<3s3sHH'
with open('chapter4/loading.gif', 'rb') as fp:
    img = memoryview(fp.read())
    
header = img[:10]
bytes(header)
```




    b'GIF89a \x00 \x00'




```python
struct.unpack(fmt, header)
```




    (b'GIF', b'89a', 32, 32)




```python
del header
del img
```

## Basic Encoders and Decoders

## Understand Encode/Decode Problems

### Coping with UnicodeEncodeError


```python
# Example 4-6 Encoding to bytes: success and error handling
city = 'São Paulo'
city.encode('utf-8')
```




    b'S\xc3\xa3o Paulo'




```python
city.encode('utf-16')
```




    b'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'




```python
city.encode('iso8859-1')
```




    b'S\xe3o Paulo'




```python
city.encode('cp437')
```


    ---------------------------------------------------------------------------

    UnicodeEncodeError                        Traceback (most recent call last)

    <ipython-input-29-064a572fd5b6> in <module>()
    ----> 1 city.encode('cp437')
    

    ~/pyenv/py3/lib/python3.5/encodings/cp437.py in encode(self, input, errors)
         10 
         11     def encode(self,input,errors='strict'):
    ---> 12         return codecs.charmap_encode(input,errors,encoding_map)
         13 
         14     def decode(self,input,errors='strict'):


    UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in position 1: character maps to <undefined>



```python
city.encode('cp437', errors='ignore')
```




    b'So Paulo'




```python
city.encode('cp437', errors='replace')
```




    b'S?o Paulo'




```python
city.encode('cp437', errors='xmlcharrefreplace')
```




    b'S&#227;o Paulo'



### Coping with UnicodeDecodeError


```python
# Example 4-7. Decoding from str to bytes: success and error handling
octets = b'Montr\xe9al'
octets.decode('cp1252')
```




    'Montréal'




```python
octets.decode('iso8859_7')
```




    'Montrιal'




```python
octets.decode('utf_8')
```


    ---------------------------------------------------------------------------

    UnicodeDecodeError                        Traceback (most recent call last)

    <ipython-input-35-afaa3d3916c5> in <module>()
    ----> 1 octets.decode('utf_8')
    

    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte



```python
# Using 'replace' error handling, the \xe9 is replaced by “�” 
a = octets.decode('utf_8', errors='replace')
```




    'Montr�al'



### SyntaxError When Modules with Unexpected Encoding
UTF-8 is the default source encoding for Python3, just as ASCII was the default for Python2.

### How to Discover the Encoding of a Byte Sequence
How do you find the encoding of a byte sequence? Short answer: you can’t. You must be told.

The package Chardet — The Universal Character Encoding Detector works to identify one of 30 supported encodings

### BOM: A useful Gremlin
If present, the BOM is supposed to be filtered by the UTF-16 codec, so that you only
get the actual text contents of the file without the leading ZERO WIDTH NO-BREAK
SPACE. The standard says that if a file is UTF-16 and has no BOM, it should be assumed
to be UTF-16BE (big-endian). However, the Intel x86 architecture is little-endian, so
there is plenty of little-endian UTF-16 with no BOM in the wild.

This whole issue of endianness only affects encodings that use words of more than one
byte, like UTF-16 and UTF-32. One big advantage of UTF-8 is that it produces the same
byte sequence regardless of machine endianness, so no BOM is needed. Nevertheless,
some Windows applications (notably Notepad) add the BOM to UTF-8 files anyway—
and Excel depends on the BOM to detect a UTF-8 file, otherwise it assumes the content
is encoded with a Windows codepage. The character U+FEFF encoded in UTF-8 is the
three-byte sequence b'\xef\xbb\xbf'. So if a file starts with those three bytes, it is likely
to be a UTF-8 file with a BOM. However, Python does not automatically assume a file
is UTF-8 just because it starts with b'\xef\xbb\xbf'.


```python
u16 = 'El Niño'.encode('utf_16')
# The \xff\xfe is BOM: byte order mark denoteing the "little endian"
u16
```




    b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'




```python
# the letter 'E', code point U+0045 (decimal 69), is encoded in byte offsets 2 and 3 as 69 and 0:
# On a big-endian CPU, the encoding would be reversed; 'E' would be encoded as 0 and 69.
list(u16)
```




    [255, 254, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]




```python
u16le = 'El Niño'.encode('utf_16le')
list(u16le)
```




    [69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]




```python
u16be = 'El Niño'.encode('utf_16be')
list(u16be)
```




    [0, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111]



## Handling Text Files
The best practice for handling text is the “Unicode sandwich”. This means
that bytes should be decoded to str as early as possible on input (e.g., when opening
a file for reading). The “meat” of the sandwich is the business logic of your program,
where text handling is done exclusively on str objects. You should never be encoding
or decoding in the middle of other processing. On output, the str are encoded to bytes
as late as possible. Most web frameworks work like that, and we rarely touch bytes when
using them. In Django, for example, your views should output Unicode str; Django
itself takes care of encoding the response to bytes, using UTF-8 by default.


```python
# Example 4-9: A platform encoding issue
open('chapter4/cafe.txt', 'w', encoding='utf-8').write('café')
```




    4



The bug: I specified UTF-8 encoding when writing the file but failed to do so when
reading it, so Python assumed the system default encoding—Windows 1252—and the
trailing bytes in the file were decoded as characters 'Ã©' instead of 'é'.


```python
# In windows output will be: 'cafÃ©'
open('chapter4/cafe.txt').read()
```




    'café'




```python
# Example 4-10: Closer inspection of Example 4-9 running on Windows reveals the bug and how to fix it
fp = open('chapter4/cafe.txt', 'w', encoding='utf-8')
fp
```




    <_io.TextIOWrapper name='chapter4/cafe.txt' mode='w' encoding='utf-8'>




```python
fp.write('café')
```




    4




```python
fp.close()
```


```python
import os
```


```python
os.stat('chapter4/cafe.txt').st_size
```




    5




```python
fp2 = open('chapter4/cafe.txt')
```


```python
fp2
```




    <_io.TextIOWrapper name='chapter4/cafe.txt' mode='r' encoding='UTF-8'>




```python
fp2.encoding
```




    'UTF-8'




```python
fp2.read()
```




    'café'




```python
fp2.close()
```

### Encoding Defaults: A Madhouse
Several settings affect the encoding defaults for I/O in Python. See the default_encodings.py script below.


```python
# Example 4-11: Exploring encoding defaults.
import sys, locale

expressions = '''
    locale.getpreferredencoding()
    type(my_file)
    my_file.encoding
    sys.stdout.isatty()
    sys.stdout.encoding
    sys.stdin.isatty()
    sys.stdin.encoding
    sys.stderr.isatty()
    sys.stderr.encoding
    sys.getdefaultencoding()
    sys.getfilesystemencoding()
'''

my_file = open('chapter4/dummy', 'w')

for exp in expressions.split():
    value = eval(exp)
    print(exp.rjust(30), '->', repr(value))
```

     locale.getpreferredencoding() -> 'UTF-8'
                     type(my_file) -> <class '_io.TextIOWrapper'>
                  my_file.encoding -> 'UTF-8'
               sys.stdout.isatty() -> False
               sys.stdout.encoding -> 'UTF-8'
                sys.stdin.isatty() -> False
                sys.stdin.encoding -> 'UTF-8'
               sys.stderr.isatty() -> False
               sys.stderr.encoding -> 'UTF-8'
          sys.getdefaultencoding() -> 'utf-8'
       sys.getfilesystemencoding() -> 'utf-8'


Note that there are four things to remember:
* If you omit the encoding argument when opening a file, the default is given by locale.getpreferredencoding() ('cp1252' in Example 4-12)
* The encoding of sys.stdout/stdin/stderr is given by the PYTHONIOENCODING environment variable, if present, otherwise it is either inherited from the console or defined by locale.getpreferredencoding() if the output/input is redirected to/from a file.
* sys.getdefaultencoding() is used internally by Python to convert binary data to/ from str; this happens less often in Python 3, but still happens.6 Changing this setting is not supported.
* sys.getfilesystemencoding() is used to encode/decode filenames (not file con‐ tents). It is used when open() gets a str argument for the filename; if the filename is given as a bytes argument, it is passed unchanged to the OS API. The Python Unicode HOWTO says: “on Windows, Python uses the name mbcs to refer to what‐ ever the currently configured encoding is.” The acronym MBCS stands for Multi Byte Character Set, which for Microsoft are the legacy variable-width encodings like gb2312 or Shift_JIS, but not UTF-8. (On this topic, a useful answer on Stack‐ Overflow is “Difference between MBCS and UTF-8 on Windows”.)

### Normalizing Unicode for Saner Comparisons


```python
s1 = 'café'
s2 = 'cafe\u0301'
s1, s2
```




    ('café', 'café')




```python
len(s1), len(s2)
```




    (4, 5)




```python
s1 == s2
```




    False




```python
from unicodedata import normalize
s1 = 'café'
s2 = 'cafe\u0301'
len(normalize('NFC', s1)), len(normalize('NFC', s2))
```




    (4, 4)




```python
len(normalize('NFD', s1)), len(normalize('NFD', s2))
```




    (5, 5)




```python
normalize('NFC', s1) == normalize('NFC', s2)
```




    True




```python
normalize('NFD', s1) == normalize('NFD', s2)
```




    True



### Case folding

### Sorting Unicode Text
