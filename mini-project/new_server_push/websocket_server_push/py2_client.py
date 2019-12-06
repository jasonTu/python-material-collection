import gevent
from gevent import monkey
monkey.patch_all()

import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('### close ###')

def client(number):
    url = 'ws://10.206.67.81:80/ws/{}'.format(number)
    print(url)
    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_close=on_close, on_error=on_error
    )
    ws.run_forever()

def run_one_wsclient(cid):
    client(cid)

def main():
    tasks = []
    for item in range(10):
        print(item)
        g_item = gevent.spawn(client, item)
        tasks.append(g_item)
    gevent.joinall(tasks)

if __name__ == '__main__':
    # main()
    run_one_wsclient(0)
