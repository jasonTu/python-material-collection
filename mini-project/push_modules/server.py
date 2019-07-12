#!/usr/bin/env python
import sys, os, time, copy
import random
import json
import urllib2, httplib
import threading
import datetime
import traceback
import logging

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/heartbeat_handler')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/persistent_handler')
# sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/httplib2-0.8-py2.7.egg')
# import httplib2, socks,socket

def main():
    count = 0
    while 1:
        count = count +1
        print count
        id = "123456"
        print "create long connection"
        subconn = httplib.HTTPConnection("10.204.244.55", timeout=600)
        subconn.request('GET', '/broadcast/sub?channel=' + id, headers={})
        res = subconn.getresponse()
        result =  res.read()
        print "long connection response %s"%result

if __name__ == "__main__":

    main()
