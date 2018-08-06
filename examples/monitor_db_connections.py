import re
import time
import commands


G_UWSGI_ROLES = ['devchannel', 'devapi', 'devreg', 'devmgmt']


def get_uwsgi_info(role):
    cmd = 'ps -ef | grep uwsgi | grep {}'.format(role)
    output = commands.getoutput(cmd)
    lines = output.split('\n')
    lines = [line for line in lines if line.find('--ignore-sigpipe') > 0]
    return lines


def get_uwsgi_master(info):
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


def main():
    cmd = 'lsof -p {} | grep mysql | grep 172-31-27-64 | grep ESTABLISHED | wc -l'
    total_cmd = 'lsof | grep uwsgi | grep mysql | grep 172-31-27-64 | grep ESTABLISHED | wc -l'
    while True:
        output = commands.getoutput(total_cmd)
        result = '%s Total Profile DB Connections: %s' % (str(time.asctime()), output)
        commands.getoutput('echo %s >> /root/db_connections.log' % result)
        for role in G_UWSGI_ROLES:
            info = get_uwsgi_info(role)
            master, slavers = get_uwsgi_master(info)
            run_cmd = cmd.format(','.join(slavers))
            output = commands.getoutput(run_cmd)
            result = '%s %s DB Connections: %s' % (str(time.asctime()), role, output)
            commands.getoutput('echo "%s" >> /root/db_connections.log' % run_cmd)
            commands.getoutput('echo %s >> /root/db_connections.log' % result)
        time.sleep(5)


if __name__ == '__main__':
    main()
