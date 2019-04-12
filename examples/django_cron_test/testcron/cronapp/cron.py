import os
import uuid
from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # A unique code
    code = 'my_app.my_cron_job'

    def do(self):
        print('I am running')
        fid = uuid.uuid4()
        os.system('touch /tmp/{}.txt'.format(fid))
