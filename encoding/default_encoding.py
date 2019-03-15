# coding: utf-8

import sys

print sys.getdefaultencoding()

a = '汉字'
b = a.decode()
b = a.encode('utf-8')
