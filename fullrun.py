from .tasks import run_crawl

import sys

scan_name = sys.argv[1]
NUM_SITES = 100000

for i in range(1, NUM_SITES, 1000):
    run_crawl.delay(scan_name, i, i+999)

