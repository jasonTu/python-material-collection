import os
import json
import struct
import socket
import asyncio
import multiprocessing

G_PROCESS = []


async def rpc(sock, in_, params):
    request = json.dumps({'in': in_, 'params': params})
    len_prefix = struct.pack('I', len(request))
    sock.send(len_prefix)
    sock.sendall(request.encode())
    len_prefix = sock.recv(4)
    print(len_prefix)
    length, = struct.unpack('I', len_prefix)
    body = sock.recv(length)
    response = json.loads(body.decode())
    return response


def main(t_num):
    loop = asyncio.get_event_loop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.195', 8080))
    pid = os.getpid()
    tasks = []
    for item in range(t_num):
        task = asyncio.ensure_future(rpc(s, 'ping', '{}.{}'.format(pid, item)))
        tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))


def prefork(p_num, t_num):
    for i in range(p_num):
        p = multiprocessing.Process(target=main, args=(t_num, ))
        G_PROCESS.append(p)
        p.start()


if __name__ == '__main__':
    prefork(50, 100)

    for p in G_PROCESS:
        p.join()
