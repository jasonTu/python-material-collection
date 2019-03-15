
# coding: gbk

'''
Set the python source code encoding to gbk in Linux with locale info:
LANG=en_US.UTF-8
LC_CTYPE=en_US.UTF-8
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
Chinese Simplified (GBK)
LC_ALL=

Use terminal as XShell 6 with GBK encoding configured.
Chinese Simplified (GBK)

'''

import sys

print sys.stdout.encoding

a = '\xd6\xd0\xb9\xfa'
print repr(a)
try:
    print a
except Exception as e:
    print e.message
