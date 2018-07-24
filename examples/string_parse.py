import re
import commands


def get_uwsgi_devchannel_info():
    cmd = 'ps -ef | grep uwsgi | grep devchannel'
    output = commands.getoutput(cmd)
    lines = output.split('\n')
    lines = [line for line in lines if line.find('--ignore-sigpipe') > 0]
    return lines


def get_devchanel_master(info):
    uwsgi_master = None
    master_pid = []
    slaver_pid = []
    for line in info:
        pid, mpid = re.split(r" +", line)[1:3]
        slaver_pid.append(pid)
        if mpid in master_pid:
            uwsgi_master = mpid
        else:
            master_pid.append(mpid)
    slaver_pid.remove(uwsgi_master)
    return uwsgi_master, slaver_pid


def kill_master(master, slavers):
    cmd = 'lsof -p {} | grep mysql | wc -l'.format(','.join(slavers))
    db_connections = commands.getoutput(cmd)
    cmd = 'kill -1 {}'.format(master)
    output = commands.getoutput(cmd)
    cmd = 'lsof -p {} | grep mysql'.format(','.join(slavers))
    output = commands.getoutput(cmd)
    print(output)
    print(cmd)
    cmd = 'lsof -p {} | grep mysql | wc -l'.format(','.join(slavers))
    output = commands.getoutput(cmd)
    print('devchannel master uwsgi pid is: %s' % master)
    print('devchannel slaver uwsgi pid is: %s' % slavers)
    print('before send master SIGHUB db connections: %s' % db_connections)
    print('after send master SIGHUB db connections: %s' % output)
    print(cmd)


def main():
    info = get_uwsgi_devchannel_info()
    mpid, slaver_pid = get_devchanel_master(info)
    kill_master(mpid, slaver_pid)


if __name__ == '__main__':
    main()
