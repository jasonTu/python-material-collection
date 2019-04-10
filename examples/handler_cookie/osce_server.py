import sys
import requests

sess = requests.Session()
login_url = 'https://10.206.67.88:4343/officescan/console/html/cgi/cgiChkMasterPwd.exe'

data = {
    'TMlogonEncrypted': 'trend#1..',
    'TxtAccount': 'root'
}
resp = sess.post(login_url, data=data, verify=False)

url = 'https://10.206.67.88:4343/officescan/console/html/cgi/cgiShowLogs.exe'
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
    'uid': '63a0328d-897e-4a90-bfcd-9a480eb3ad38',
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
    'uid': '63a0328d-897e-4a90-bfcd-9a480eb3ad38',
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
    'uid': '63a0328d-897e-4a90-bfcd-9a480eb3ad38',
    'id': 12954,
    'Ticket': ticket
}
print data
resp = sess.post(url, data=data, verify=False)
print resp.status_code
print resp.content

sys.exit()

cookies = '''session_expired=no; DisabledIds=9999.;FeatureEnableState=enableAntiBody@1|enableCCFR@1|enableCfw@1|enableDcs@1|enableSorting@0|enableSpy@1|enableVirus@1|HasAvAddSvc@1|installWSS@1|enableDLP@0|sqldbMode@0|enableIPv6@1|w2ksupport@0|;LogonUser=root; ReadOnlyIds=8.56.; enableRba=1; key=243741516831420;session=200; LANG=zh_CN; PHPSESSID=061ndtklb1qt7ipgb8hhu2f7e1; cname=dashBoard;lastID=34; lastTab=1; theme=default; un=425fba925bfe7cd8d80a8d5f441be863;userID=1;wids=modOSCERansomwareDetectionsSummary%2CmodOSCEOutbreakStatus%2CmodOSCERansomwareDetectionsOverTime%2CmodOSCEDetectionStatus%2CmodOSCENetworkedComputers%2CmodOSCEUpdateStatus%2C;stamp=85426147; timestamp=1554909521; PHPSESSID=061ndtklb1qt7ipgb8hhu2f7e1;un=425fba925bfe7cd8d80a8d5f441be863; userID=1; LANG=zh_CN;wids=modOSCERansomwareDetectionsSummary%2CmodOSCEOutbreakStatus%2CmodOSCERansomwareDetectionsOverTime%2CmodOSCEDetectionStatus%2CmodOSCENetworkedComputers%2CmodOSCEUpdateStatus%2C;lastID=34; cname=dashBoard; theme=default; lastTab=1'''
# csv=0&txtDateTo=&txtDateFrom=&optTime=1&optRange=3&chkTypeManual=1&chkTypeScheduled=1&chkTypeScanNow=1&chkStatusCompleted=1&chkStatusStopped=1&chkStatusInterrupted=1&uid=63a0328d-897e-4a90-bfcd-9a480eb3ad38&id=12953
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
    'uid': '63a0328d-897e-4a90-bfcd-9a480eb3ad38',
    'id': '12953'
}
headers = {}
headers['Cookie'] = cookies
print data
resp = requests.post(url, data=data, verify=False)
print resp.status_code
print resp.content
ticket = str(resp.json()['REQUEST_TICKET'])
data = {
    'id': '12122',
    'Ticket': ticket
}
print data
resp = requests.post(url, data=data, verify=False, headers=headers)
print resp.status_code
print resp.content
# csv=0&txtDateTo=&txtDateFrom=&optTime=1&optRange=3&chkTypeManual=1&chkTypeScheduled=1&chkTypeScanNow=1&chkStatusCompleted=1&chkStatusStopped=1&chkStatusInterrupted=1&uid=63a0328d-897e-4a90-bfcd-9a480eb3ad38&Ticket=84965302&id=12954
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
    'uid': '63a0328d-897e-4a90-bfcd-9a480eb3ad38',
    'id': 12954,
    'Ticket': ticket
}
data = {
    'csv': 0,
    'optTime': 1,
    'optRange': 3,
    'chkTypeManual': 1,
    'uid': '63a0328d-897e-4a90-bfcd-9a480eb3ad38',
    'id': 12954,
    'Ticket': ticket
}
print data
resp = requests.post(url, data=data, verify=False, headers=headers)
print resp.status_code
print resp.content
