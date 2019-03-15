
# coding: utf-8

import sys

print sys.stdout.encoding

# a = 'Ö¹úkk'
a = '中国'
print repr(a)
try:
    print a
except Exception as e:
    print e.message
