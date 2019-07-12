import httplib
import json
import time
import ssl

def sub():
    push_server = 'beta-devmgmt01.beta.cloudedge.trendmicro.com'
    guid = '123456'
    subconn = httplib.HTTPSConnection(push_server, timeout=600,
            context=ssl._create_unverified_context())
    subconn.request('GET', '/broadcast/sub?channel=' + guid)
    res = subconn.getresponse()
    result =  json.loads(res.read())


if __name__ == '__main__':
    while True:
        sub()
