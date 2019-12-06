#!/usr/bin/env python
import websocket
import ssl
import sys, os, time, copy
import random
import json
import urllib2, httplib
import threading
import datetime
from daemon import Daemon
from common_error import *
import DevClient

from persistent_handler import cmd_all

DevClient.init_logger()
import traceback
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/heartbeat_handler')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/persistent_handler')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/httplib2-0.8-py2.7.egg')

import httplib2, socks
import socket

import ctypes
libc = ctypes.cdll.LoadLibrary('libc.so.6')
res_init = libc.__res_init

mapping_heartbeat_module_name = {}
mapping_heartbeat_name_module = {}
#mapping_persistent_name_module = {}
#mapping_persistent_module_name = {}

reload(sys)
sys.setdefaultencoding('utf-8')

def refresh_dns():
    try:
        res_init()
    except Exception, e:
        logging.error(traceback.format_exc())

def SetLastHeartTime():
    fileName = "/usr/vtm/tmp/heartbeat.txt";
    try:
        infile = open(fileName, 'wb')
        dt = datetime.datetime.utcnow()
        infile.write(str(dt))
        infile.close()
    except:
        print "except"
        pass
import itertools
def anyTrue(predicate, sequence):
    return True in itertools.imap(predicate, sequence)
def endsWith(s, *endings):
    return anyTrue(s.endswith, endings)

for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/heartbeat_handler'):
    if endsWith(filename, '.py'):
        pluginname = filename.replace('.py', '')
        try:
            module = __import__(pluginname)
            mapping_heartbeat_module_name[module] = pluginname
            mapping_heartbeat_name_module[pluginname] = module
            #heartbeat_plugin_module.append(module)

        except Exception, e:
            logging.error(traceback.format_exc())
            continue
"""
for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/persistent_handler'):
    if endsWith(filename, '.py'):

        pluginname = filename.replace('.py', '')

        try:
            module = __import__(pluginname)
            mapping_persistent_module_name[module] = pluginname
            mapping_persistent_name_module[pluginname] = module
            #persistent_plugin_module.append(module)

        except Exception, e:
            logging.error(traceback.format_exc())
            continue
"""

class Heartbeat(threading.Thread):
    heartbeat_begin = 0
    def run(self):
        if self.heartbeat_begin == 0:
            self.heartbeat_begin = time.time()
        while 1:
            #add ETH0's mac to heartbeat by jim
            serial_number_mac = None
            request_dict = {}
            for key in mapping_heartbeat_module_name:
                tmp = key.get_api_request()
                if not tmp == None:
                    for item in tmp:
                        if item['api'] == 'guid_check':
                            serial_number_mac = item['param']

                request_dict[mapping_heartbeat_module_name[key]] = tmp

            logging.debug("request_dict %r",request_dict)

            #add ETH0's mac to heartbeat by jim
            if not serial_number_mac == None:
                resp = DevClient.do_api_request(api_name='heartbeat', \
                    data={u'content' : request_dict},header_list=[('serial_number',serial_number_mac)])
            else:
                resp = DevClient.do_api_request(api_name='heartbeat', \
                    data={u'content' : request_dict})

            logging.debug('[Heartbeat thread]get response : %s', str(resp))

            if resp['error_code'] != 0 :
                if resp['error_code'] == 1 or resp['error_code'] == 4:
                    logging.info('[Heartbeat thread]no such device in skynet, set device unregistered')
                    DevClient.set_device_unregistered_inenc()
                    try:
                        cmd_all.resp_handler(CMD_DEV_UNREGISTER, None)
                    except Exception, e:
                        logging.error(traceback.format_exc())
                        logging.error('do cmd_all.resp_handler CMD_DEV_UNREGISTER failed')
                        pass

                if resp['error_code'] == 25:
                    logging.info('[Heartbeat thread]connection request to skynet failed, maybe newwork error now')
                    logging.info('[Heartbeat thread]run offline callback')

                    for key in mapping_heartbeat_module_name:
                        try:
                            key.offline_handler()
                        except Exception, e:
                            logging.error(traceback.format_exc())
                            logging.error('[Heartbeat thread]call offline_handler error')
                            continue

                start_sleep = time.time()
                sleep_time = DevClient.HEARTBEAT_INTERVAL - (start_sleep - self.heartbeat_begin)% DevClient.HEARTBEAT_INTERVAL
                logging.error('[Heartbeat thread]get error from skynet heartbeat api, sleep %s second', sleep_time)

                time.sleep(sleep_time)

                continue

            resp_dict = json.loads(resp[OPTION_HTTP_BODY])
            logging.debug(str(resp_dict))

            for key in resp_dict:
                try:
                    mapping_heartbeat_name_module[key].resp_handler(resp_dict[key])
                except Exception, e:
                    logging.error(traceback.format_exc())
                    logging.error('[Heartbeat thread]call resp_handler failed')
                    continue

            logging.debug('[Heartbeat thread]get success from skynet heartbeat api, sleep %s second', DevClient.HEARTBEAT_INTERVAL)
            #write heart beat time
            SetLastHeartTime()

            start_sleep = time.time()
            sleep_time = DevClient.HEARTBEAT_INTERVAL - (start_sleep - self.heartbeat_begin)% DevClient.HEARTBEAT_INTERVAL
            time.sleep(sleep_time)

class LongPollingRespHandler(threading.Thread):
    def __init__(self, guid, instance_ip, prefix_id, callback, param, cookie=None):
        threading.Thread.__init__(self)
        self.guid = guid
        self.instance_ip = instance_ip
        self.prefix_id = prefix_id
        self.callback = callback
        self.param = param
        self.cookie = cookie

    def run(self):
        #result = mapping_persistent_name_module[self.callback].resp_handler(self.param)
        ##########handle rename and unregister cmd#################
        if self.callback == CMD_DEV_RENAME:
            try:
                logging.debug('[LongPollingRespHandler thread]receive rename cmd')
                DevClient.set_device_name(self.param[OPTION_NAME])
            except Exception, e:
                logging.error(e.message)
                logging.error('[LongPollingRespHandler thread]can not rename cause the param has the wrong key')
                pass
        elif self.callback == CMD_DEV_UNREGISTER:
            try:
                logging.debug('[LongPollingRespHandler thread]receive unregister cmd')
                DevClient.set_device_unregistered_inenc()
            except Exception, e:
                logging.error(e.message)
                logging.error('[LongPollingRespHandler thread]set_device_unregistered_inenc failed')
                pass
        else:
            pass
        ###########################################################
        result = cmd_all.resp_handler(self.callback, self.param)

        logging.debug(str(result))

        url_string = 'https://' + DevClient.push_server + '/broadcast/pub?channel=' + self.guid + self.prefix_id
        logging.debug(url_string)

        count = 0
        while count < 5:
            count += 1
            req =urllib2.Request(url_string)
            if self.cookie:
                logging.debug('[LongPollingRespHandler thread]add cookie to http header')
                req.add_header('cookie', self.cookie)

            opener = urllib2.build_opener(DevClient.proxy_handler)
            try:
                logging.debug('[LongPollingRespHandler thread]try to push result to skynet')
                res = opener.open(req, json.dumps(result), timeout=DevClient.OTHERAPI_REQUEST_TIMEOUT)

                push_module_resp = json.loads(res.read())
                logging.debug('[LongPollingRespHandler thread]get push_module resp : %s', str(push_module_resp))
                if push_module_resp['subscribers'] != '0':
                    logging.debug('[LongPollingRespHandler thread]skynet subscribe this channel')
                    break

                logging.debug('[LongPollingRespHandler thread]no active subscribers in this channel, retry times is %s', str(count))
                time.sleep(1)
                continue

            except Exception, e:
                logging.error(traceback.format_exc())
                time.sleep(1)
                continue

class LongPolling(threading.Thread):
    def run(self):
        record_instance_ip_serial = random.randint(1, 100)
        cookie = ''
        cookie_timeout_count = 0
        content_data = None
        last_prefix_id = ''  ##remember the last prefix_id to avoid getting same cmd twice
        last_cmd_time = 0
        while 1:
            guid = None
            record_instance_ip_serial += 1
            if record_instance_ip_serial == 1000000:
                record_instance_ip_serial = random.randint(1, 100)
            try:
                #if not guid:
                ## get device info everytime, cause we want know the last conn status in real time.
                if not content_data:
                    content_data = DevClient.get_device_info()
                guid = content_data['guid']
                if not guid:
                    content_data = None
                    logging.error('[LongPolling thread]device not in correct status, can not get the info')
                    logging.error('[LongPolling thread]sleep long time to wait for device status come back, and then re-connect longpolling')
                    time.sleep(int(DevClient.HEARTBEAT_INTERVAL/2))
                    continue
                logging.debug('[LongPolling thread]longpolling start, at first call record_instance_ip api')
                #opener = urllib2.build_opener(DevClient.proxy_handler)
                opener = DevClient.buildValidatingOpener(DevClient.CA_CERT, DevClient.proxy_handler)
                if cookie == '':
                    opener.addheaders = [(DevClient.HEADER_GUID, guid), (DevClient.HEADER_SERIAL, str(record_instance_ip_serial))]

                else:
                    opener.addheaders = [(DevClient.HEADER_GUID, guid), (DevClient.HEADER_SERIAL, str(record_instance_ip_serial)), \
                    ('cookie', cookie)]

                res = opener.open('https://' + DevClient.push_server + '/DevReg/V1.0/record_instance_ip', timeout=DevClient.OTHERAPI_REQUEST_TIMEOUT)
                #logging.debug(str(res.info()))
                try:
                    tmp_cookie = res.info().getheader('Set-Cookie')
                    if not tmp_cookie:
                        pass
                    else:
                        cookie = tmp_cookie
                        logging.debug('[LongPolling thread]get new sticky session from record_instance_ip api')
                        logging.debug(str(cookie))
                except Exception, e:
                    cookie = ''
                    logging.debug('not get sticky session, cmd response may return the wrong instance')

                # Websocket based push cmd
                logging.info('[Websocket thread] url is')
                logging.info('[Websocket thread]longpolling contiune, call nginx push stream channel, wait for cmd')
                url = 'wss://{}/broadcast/sub?channel={}'.format(DevClient.push_server, guid)
                logging.info('[Websocket thread] url is %s', url)
                def on_message(ws, message):
                    logging.info('[Websocket thread]get cmd: %s', message)
                    result = json.loads(message)
                    logging.info('[Websocket thread]get result: %s', result)
                    if result["callback_name"] == "ssh_tunnel":
                        result2 = copy.deepcopy(result)
                        result2["callback_data"]["pem"] = "*"
                        result2["callback_data"]["cepasswd"] = "*"
                        current_cmd_time = int(time.time())
                        logging.debug('[Websocket thread]get cmd one time:%s', str(result2))
                    else:
                        current_cmd_time = int(time.time())
                        logging.debug('[Websocket thread]get cmd one time:%s', str(result))

                    logging.info('[Websocket thread]before get data from result')
                    try:
                        instance_ip   = result['instance_ip']
                        prefix_id     = result['prefix_id']
                        callback_name = result['callback_name']
                        callback_data = result['callback_data']
                    except Exception, e:
                        logging.error(traceback.format_exc())
                        logging.error('[Websocket thread]content from push server is not correct format')
                        return
                    logging.info('[Websocket thread]after get data from result')

                    logging.info('[Websocket thread]prefix_id: %s', prefix_id)
                    # global last_prefix_id
                    # logging.info('[Websocket thread]last_prefix_id: %s', last_prefix_id)

                    #logging.info('[Websocket thread]last_prefix_id: %s', last_prefix_id)
                    # logging.info('[Websocket thread]prefix_id: %s', prefix_id)
                    # logging.info('[Websocket thread]prefix_id is %s, last_prefix_id is %s', prefix_id, last_prefix_id)

                    # if prefix_id == last_prefix_id and abs(current_cmd_time - last_cmd_time) < 60:
                    #     logging.info('[Websocket thread]get same cmd twice, skip LongPollingRespHandler')
                    #     return
                    # else:
                    #     logging.info('[Websocket thread]get new cmd, do LongPollingRespHandler')
                    #     last_prefix_id = prefix_id
                    #     last_cmd_time = int(time.time())
                    logging.info('[Websocket thread]get new cmd, do LongPollingRespHandler')

                    logging.info('[Websocket thread]Before call LongPollingRespHandler')
                    resp_handler = LongPollingRespHandler(guid, instance_ip, prefix_id, callback_name, callback_data, cookie)
                    resp_handler.start()
                    logging.info('[Websocket thread]After call LongPollingRespHandler')

                def on_error(ws, error):
                    logging.info('[Websocket thread]ws error: %s', error)

                def on_close(ws):
                    logging.info('[Websocket thread]ws close')

                ws = websocket.WebSocketApp(url, on_message=on_message, on_close=on_close, on_error=on_error)
                ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

            except Exception, e:
                logging.error(traceback.format_exc())
                ####if timeout, we reconnet immediately, other error, we should sleep specified time
                # Actually websocket channle will never timeout, because the lib already provide keep-alive
                logging.info('[Websocket thread]timeout or other http request error, re-connect again')

                cookie_timeout_count += 1
                if cookie_timeout_count == 240: # we use one cookie in 8 hours, then we get new one, 8*60/2 = 240
                    cookie = ''
                    cookie_timeout_count = 0
                    logging.info('[LongPolling thread]clear the cookie, make elb reload balance')

                content_data = DevClient.get_device_info()
                if content_data[OPTION_LASTCOMM_STATUS] == 'succeed':
                    logging.debug('[LongPolling thread]sleep 1 second')
                    time.sleep(1)
                else:
                    logging.error('[LongPolling thread]sleep long time to wait for network back')
                    time.sleep(2)
                    cookie = ''
                refresh_dns()
                continue

###############################################################################

class SkynetDaemon(Daemon):
    def run(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        logging.debug('Heartbeat daemon run')
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            logging.error('pid is not existed, something wrong with create pid file, no need to run daemon, exit')
            return
        else:
            logging.debug('Heartbeat process start, pid is %s', str(pid))

        try:
            socket.setdefaulttimeout(120)

            heartbeat = Heartbeat()
            logpolling = LongPolling()

            heartbeat.start()
            logpolling.start()

            heartbeat.join()
            logpolling.join()

        except Exception, e:
            logging.error('threads crash with unexcepted error, daemon exit')

        return

if __name__ == "__main__":
    daemon = SkynetDaemon(os.path.dirname(os.path.realpath(__file__)) + '/devreg_daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
                daemon.start()
        elif 'stop' == sys.argv[1]:
                daemon.stop()
        elif 'restart' == sys.argv[1]:
                daemon.restart()
        else:
                logging.error("Unknown command")
                sys.exit(2)

        sys.exit(0)
    else:
        #print "usage: %s start|stop|restart" % sys.argv[0]
        logging.error('usage: Heartbeat.py start|stop|restart')
        sys.exit(2)
