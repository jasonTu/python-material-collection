import time
import commands

def push_cmd(number):
    cmd_t = 'curl http://localhost/pub?id={} -d "{}"'
    data = {
        "hostname": "macintoshdemacbook-air.local",
        "time": "2016-05-07T12:02:34",
        "channels": 0,
        "wildcard_channels": 0,
        "published_messages": 0,
        "stored_messages": 0,
        "messages_in_trash": 0,
        "channels_in_trash": 0,
        "subscribers": 0,
        "uptime": 19755,
        "by_worker": [{
            "pid": "21117",
            "subscribers": 0,
            "uptime": 19755
        }]
    }
    for i in range(number):
        cmd = cmd_t.format(i, data)
        status, output = commands.getstatusoutput(cmd)


if __name__ == '__main__':
    while True:
        push_cmd(10)
        time.sleep(5)
