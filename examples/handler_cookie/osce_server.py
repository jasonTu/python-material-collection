import sys
import requests

sess = requests.Session()
host = '10.206.67.88'
uid = '63a0328d-897e-4a90-bfcd-9a480eb3ad38'
login_url = 'https://{}:4343/officescan/console/html/cgi/cgiChkMasterPwd.exe'.format(host)

data = {
    'TMlogonEncrypted': 'trend#1..',
    'TxtAccount': 'root'
}
resp = sess.post(login_url, data=data, verify=False)

url = 'https://{}:4343/officescan/console/html/cgi/cgiShowLogs.exe'.format(host)
data = {
    'csv': '0',
    'txtDateTo': None,
    'txtDateFrom': None,
    'optTime': '1',
    'optRange': '3',
    'chkTypeManual': '1',
    'chkTypeScheduled': '1',
    'chkTypeScanNow': '1',
    'chkStatusStopped': '1',
    'chkStatusInterrupted': '1',
    'uid': uid,
    'id': '12953'
}
print data
resp = sess.post(url, data=data, verify=False)
print resp.status_code
print resp.content

ticket = str(resp.json()['REQUEST_TICKET'])
data = {
    'id': '12122',
    'Ticket': ticket
}
print data
resp = sess.post(url, data=data, verify=False)
print resp.status_code
print resp.content

data = {
    'csv': 0,
    'optTime': 1,
    'optRange': 3,
    'chkTypeManual': 1,
    'uid': uid,
    'id': 12954,
    'Ticket': ticket
}
data = {
    'csv': 0,
    'txtDateTo': None,
    'txtDateFrom': None,
    'optTime': 1,
    'optRange': 3,
    'chkTypeManual': 1,
    'chkTypeScheduled': 1,
    'chkTypeScanNow': 1,
    'chkStatusStopped': 1,
    'chkStatusInterrupted': 1,
    'uid': 'uid',
    'id': 12954,
    'Ticket': ticket
}
print data
resp = sess.post(url, data=data, verify=False)
print resp.status_code
print resp.content
