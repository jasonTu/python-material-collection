import re
import time
import json
from datetime import datetime


class DBUtils:

    def __init__(self):
        try:
            from src.database import DatabaseMgr
            from src.database import ConnectionMgr
            con = ConnectionMgr.Connection('/etc/skynet/skynet-env.ini')
            storage_conn = con.getProfileStorage()
            self.storage = DatabaseMgr.RDSMgrNoPool(storage_conn)
            session_conn = self.get_session_storage(con)
            self.session_storage = DatabaseMgr.RDSMgrNoPool(session_conn)
        except:
            pass

    def get_session_storage(self, conn):
        address = '{dialect}+{driver}://{user}:{password}@{host}/{dbname}'
        dialect = conn.config.getValue('SessionDB', 'DB_DIALECT')
        driver = conn.config.getValue('SessionDB', 'DB_DRIVER')
        user = conn.config.getValue('SessionDB', 'DB_ACCOUNT')
        password = conn.config.getValue('SessionDB', 'DB_PASSWORD')
        host = conn.config.getValue('SessionDB', 'DB_HOST')
        dbname = conn.config.getValue('SessionDB', 'DB_DBNAME')
        return address.format(
            dialect=dialect, driver=driver, user=user, password=password,
            host=host, dbname=dbname
        )

    def get_online_session_info(self):
        '''
        session_data sample:
        SESSION_CLIENT_REAL_IP|s:13:"10.64.194.133";IsUserLoggedIn|b:1;IsSSO|b:0;
        mode|i:0;userId|s:15:"admin@cloud.com";userName|s:15:"admin@cloud.com";
        email|s:15:"admin@cloud.com";companyId|s:5:"cloud";
        timeZone|s:13:"Asia/Shanghai";isReadOnly|b:0;companyName|s:5:"cloud";
        deviceType|s:6:"CE100C";language|s:5:"en_US";
        CSRFT|s:128:"d5c7cdcc81f665dca736f889c28337db44c004d168456c29821924dd7336db529ec42ef934ec08ae114a594420b6fbc392248d6f613af34a36f170ac8864f951";
        UserName|s:15:"admin@cloud.com";CompanyName|s:5:"cloud";
        CompanyId|s:5:"cloud";uniqueid|s:32:"0b390f201bd8883695abe0bb8ad1252a";
        uid|s:1:"1";
        '''
        ret = []
        sql = 'select session_data, session_expiry from session'
        result_list = self.session_storage.engine.execute(sql).fetchall()
        return result_list

    def online_analysis_session_info(self):
        reg_username = r'UserName\|s:(\d{1,2}):"(?P<username>.*?)"'
        reg_comid = r'CompanyId\|s:(\d{1,2}):"(?P<comid>.*?)"'
        ts_now = int(time.time())
        result_list = self.get_online_session_info()
        for item in result_list:
            session_data, session_expiry = item[0], item[1]
            username_ret = re.search(reg_username, session_data)
            if ts_now > session_expiry:
                print('Expired, session_expiry: %d, ts_now: %d' % (session_expiry, ts_now))
            if username_ret:
                print(username_ret.group('username'))
            comid_ret = re.search(reg_comid, session_data)
            if comid_ret:
                print(comid_ret.group('comid'))

    def get_all_schedule_bakcups(self):
        ret = []
        all_data = []
        sql = 'select row_key, updatingSetting from companies'
        result_list = self.storage.engine.execute(sql).fetchall()
        for item in result_list:
            company_id = item[0]
            settings = item[1]
            if settings is not None:
                settings_obj = json.loads(settings)
                all_data.append({company_id: settings_obj})
                bk_obj = settings_obj.get('AUTOBK')
                if bk_obj is not None and bk_obj['IsEnable'] == 'yes':
                    ret.append({company_id: bk_obj})
        with open('updatingSettings.json', 'w+') as fp:
            fp.write(json.dumps(all_data, indent=2))
        return ret

    def get_active_schedule_backups(self, backups, hour):
        act_backups = []
        now = datetime.now()
        for back in backups:
            company_id = back.keys()[0]
            settings = back[company_id]
            run_hour = int(settings['Runtime'].split(':')[1])
            run_date = int(settings['Runtime'].split(':')[0])
            if settings['Frequency'] == 'daily':
                if run_hour == hour:
                    act_backups.append(back)
            elif settings['Frequency'] == 'weekly':
                if run_date == now.weekday() and run_hour == hour:
                    act_backups.append(back)
            elif settings['Frequency'] == 'monthly':
                if run_date == now.day and run_hour == hour:
                    act_backups.append(back)
        return act_backups

    def get_online_bk_data(self):
        return self.get_all_schedule_bakcups()

    def get_offline_bk_data(self, file_path):
        ret = []
        with open(file_path) as fp:
            raw_data = json.load(fp)
        for item in raw_data:
            company_id = item.keys()[0]
            settings = item[company_id]
            bk_obj = settings.get('AUTOBK')
            if bk_obj is not None and bk_obj['IsEnable'] == 'yes':
                ret.append({company_id: bk_obj})
        return ret

    def online_analysis(self):
        data = self.get_online_bk_data()
        return self.get_active_schedule_backups(data, 10)

    def offline_analysis(self, file_path):
        data = self.get_offline_bk_data(file_path)
        for i in range(24):
            print i, self.get_active_schedule_backups(data, i)


if __name__ == '__main__':
    dbut = DBUtils()
    # dbut.online_analysis()
    # dbut.offline_analysis('updatingSettings.json')
    dbut.online_analysis_session_info()
