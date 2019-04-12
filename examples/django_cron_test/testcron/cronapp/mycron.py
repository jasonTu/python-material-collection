import os
import uuid

def test_cron():
    fid = str(uuid.uuid4())
    os.system('touch /tmp/{}.txt'.format(fid))
