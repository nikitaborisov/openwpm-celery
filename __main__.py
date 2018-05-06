import sys

from .tasks import run_crawl
import os.path

scan_name = sys.argv[1]
NUM_SITES = 100000


for i in range(1, NUM_SITES, 1000):
    if len(sys.argv) > 2 and sys.argv[2] == "missing":
        if os.path.exists("/efs/crawls/{}/{}-{}".format(scan_name, i, i+999)):
            continue
    run_crawl.delay(scan_name, i, i+999)



