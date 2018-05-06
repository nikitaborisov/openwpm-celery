from __future__ import absolute_import, unicode_literals
from celery import Celery
from  . import celeryconfig as config

app = Celery('openwpm-redis', 
		broker = 'redis://wpm-celery-q.gxtufv.ng.0001.use2.cache.amazonaws.com:6379/0',
		backend = 'redis://wpm-celery-q.gxtufv.ng.0001.use2.cache.amazonaws.com:6379/1',
             include=['aws_cel.tasks'],
             config_source = config)


if __name__ == '__main__':
    app.start()

