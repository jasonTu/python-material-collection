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
    if uwsgi_master in slaver_pid:
        slaver_pid.remove(uwsgi_master)
    return uwsgi_master, slaver_pid


def kill_master(master, slavers):
    cmd = 'lsof -p {} | grep mysql | grep ESTABLISHED'.format(','.join(slavers))
    db_connections = commands.getoutput(cmd)
    db_conn_num = len(db_connections.split('\n'))
    cmd = 'kill -1 {}'.format(master)
    output = commands.getoutput(cmd)
    cmd = 'lsof -p {} | grep mysql'.format(','.join(slavers))
    output = commands.getoutput(cmd)
    print(output)
    print(cmd)
    cmd = 'lsof -p {} | grep mysql | grep ESTABLISHED'.format(','.join(slavers))
    output = commands.getoutput(cmd)
    lines = output.split('\n')
    if '' in lines:
        lines.remove('')
    conn_num = len(lines)
    print('devchannel master uwsgi pid is: %s' % master)
    print('devchannel slaver uwsgi pid is: %s' % slavers)
    print('before send master SIGHUB db connections: %s' % db_conn_num)
    print('after send master SIGHUB db connections: %s' % conn_num)
    print(cmd)
    kill_master_times = 30
    while conn_num != 0:
        if kill_master_times > 0:
            kill_cmd = 'kill -1 {}'.format(master)
            commands.getoutput(kill_cmd)
            kill_master_times -= 1
        info = get_uwsgi_devchannel_info()
        mid, sids = get_devchanel_master(info)
        print('devchannel master uwsgi pid is: %s' % mid)
        print('devchannel slaver uwsgi pid is: %s' % sids)
        print
        output = commands.getoutput(cmd)
        lines = output.split('\n')
        if '' in lines:
            lines.remove('')
        conn_num = len(lines)
        print('after send master SIGHUB db connections: %s' % conn_num)
        if int(conn_num) > 60:
            print(output)


def main():
    info = get_uwsgi_devchannel_info()
    mpid, slaver_pid = get_devchanel_master(info)
    kill_master(mpid, slaver_pid)


if __name__ == '__main__':
    main()
