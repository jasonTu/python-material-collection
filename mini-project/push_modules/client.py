#!/usr/bin/env python
import os, sys, string, random, datetime
from itertools import islice, imap, repeat
import urllib2, httplib
import json
import time
# import slogging as logging
import logging
import ConfigParser
import traceback
import ssl
import time, thread

def rand_token(length = 32):
    chars = set(string.ascii_letters + string.digits)
    char_gen = (c for c in imap(os.urandom, repeat(1)) if c in chars)
    return ''.join(islice(char_gen, None, length))

def push_devcmd(node):
    print node
    prefix_id = str(rand_token(8))
    opener = urllib2.build_opener()
    id = "123456"
    param = {}
    param['prefix'] = prefix_id
    param['data'] = "test"
    result = opener.open('http://10.206.66.74/broadcast/pub?channel=' + id,json.dumps(param))
    res = result.read()
    logging.info(res)

if __name__ == '__main__':
    for i in range(1,20):
        thread.start_new_thread(push_devcmd, (i,))
    time.sleep(600)
