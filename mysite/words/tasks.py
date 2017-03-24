from __future__ import absolute_import

from celery import shared_task

from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def test(param):
    logger.info("Testing")
    return 'The test task executed with argument "%s" ' % param

# call with executeRequestAsync.delay(request object)
@task(name="executeRequestAsync")
def executeRequestAsync(request):
    logger.info("Request executing")
    request.execute()

@periodic_task(run_every=(crontab(minute='*/1')), name="testPeriodic", ignore_result=True)
def testPeriodic():
    logger.info("Testing Periodic")
    
queue = []    
@periodic_task(run_every=(crontab(minute='*/10')), name="emailQueue", ignore_result=True)
def emailQueue():
    for item in queue():
        if (csvGenerated(item[0])):
            queue.remove(item)
            sendEmail(item[1])
    logger.info("Testing Periodic")
    
#program flow:
#get user input
#create Request object containing a hash and email
#Request.execute() to start the processing
#Request.queue() to add a (hash,email) to the queue
#emailQueue runs periodically, emailing users if the hash exists as a csv