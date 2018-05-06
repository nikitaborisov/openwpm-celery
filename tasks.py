
from .celery import app
import os
import subprocess
import time
import sqlite3
import shutil

@app.task
def run_crawl(scan_name, start, end):
    scan_dir = "/tmp/scan" + str(time.time())

    subprocess.check_call(["python", "crawl_aws.py", scan_dir, str(start), str(end)])
    with sqlite3.connect(scan_dir + "/crawl-data.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute('select count(*) from site_visits')
        count = cursor.fetchone()[0]
        if count != end-start + 1:
            raise ValueError("Wrong number of site visits: {}".format(count))
    with open(scan_dir + "/good", 'w'):
        pass
    new_dir = "/efs/crawls/{}/{}-{}/{}-{}".format(scan_name, start, end, 
        subprocess.check_output(['ec2metadata', '--public-ipv4']).strip(), time.time())
    os.makedirs(new_dir)
    shutil.copyfile(scan_dir + "/crawl-data.sqlite", new_dir + "/crawl-data.sqlite")
    shutil.copyfile(scan_dir + "/openwpm.log", new_dir + "/openwpm.log")
