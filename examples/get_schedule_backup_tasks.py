import json
from datetime import datetime


class DBUtils:

    def __init__(self):
        try:
            from src.database import DatabaseMgr
            from src.database import ConnectionMgr
            con = ConnectionMgr.Connection('/etc/skynet/skynet-env.ini')
            storageConnection = con.getProfileStorage()
            self.storage = DatabaseMgr.RDSMgrNoPool(storageConnection)
        except:
            pass

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
    dbut.offline_analysis('updatingSettings.json')
