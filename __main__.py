import sys

from .tasks import run_crawl
import os.path

scan_name = sys.argv[1]
NUM_SITES = 1000000
BATCH = 500


for i in range(1, NUM_SITES, BATCH):
    if len(sys.argv) > 2 and sys.argv[2] == "missing":
        if os.path.exists("/efs/crawls/{}/{}-{}".format(scan_name, i, i+BATCH-1)):
            continue
    run_crawl.delay(scan_name, i, i+BATCH-1)



