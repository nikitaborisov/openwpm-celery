
from .celery import app
import os
from subprocess import check_call, check_output
import time
import sqlite3
import shutil
import sys

DB_NAME = "crawl-data.sqlite"

COPY_FILES = [ DB_NAME, "openwpm.log" ]
COPY_DIRS = [ "javascript.ldb" ]

GIT_SSH_PREFIX = "GIT_SSH_COMMAND='ssh -i /efs/ssh/wpm_deploy_key' "

@app.task
def run_crawl(scan_name, start, end, commit=None):
    try:
        if commit:
            check_call(GIT_SSH_PREFIX + "git fetch", shell=True)
            check_call(["git", "checkout", commit])
        scan_dir = "/tmp/scan" + str(time.time())

        check_call(["python", "crawl_aws.py", scan_dir, str(start), str(end)])
        with sqlite3.connect(scan_dir + "/" + DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('select count(*) from site_visits')
            count = cursor.fetchone()[0]
            if count != end-start + 1:
                raise ValueError("Wrong number of site visits: {}".format(count))
        with open(scan_dir + "/good", 'w'):
            pass
        ipv4 = check_output(['ec2metadata', '--public-ipv4']).strip() 
        new_dir = "/efs/crawls/{}/{}-{}/{}-{}".format(scan_name, start, end,
                                                      ipv4, time.time())
        os.makedirs(new_dir)
	
        for filename in COPY_FILES:
            shutil.copy(scan_dir + "/" + filename, new_dir + "/" + filename)
        for dirname in COPY_DIRS:
            shutil.copytree(scan_dir + "/" + dirname, new_dir + "/" + dirname)
        with open(new_dir + "/finished", 'w'):
            pass
    except Exception as e:
        raise ValueError, "Runtime exception %s" % e, sys.exc_info()[2]

