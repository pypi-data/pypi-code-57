# import logging
# import time
# import threading
#
# import django_rq
#
# from django.conf import settings
#
# from remo_app.remo.use_cases import jobs
#
# logger = logging.getLogger('remo_app')
#
#
# def schedule_jobs():
#     if not settings.INSIDE_TEST:
#         threading.Thread(target=register_scheduled_jobs).start()
#
#
# def register_scheduled_jobs():
#     time.sleep(15)
#
#     logger.debug('Empty scheduled jobs')
#     scheduler = django_rq.get_scheduler()
#     conn = django_rq.get_connection()
#     conn.delete(scheduler.scheduled_jobs_key)
#
#     logger.debug('Register scheduled jobs')
#     for job in jobs.all_jobs:
#         scheduler.cron(settings.RQ_CRON_SCHEDULER, func=job)
#
# # Sample
# # scheduler.cron(
# #     "0 * * * *",  # A cron string (e.g. "0 0 * * 0")
# #     func=update_dataset_statistics,  # Function to be queued
# #     args=[arg1, arg2],  # Arguments passed into function when executed
# #     kwargs={'foo': 'bar'},  # Keyword arguments passed into function when executed
# #     repeat=10,  # Repeat this number of times (None means repeat forever)
# #     queue_name=queue_name,  # In which queue the job should be put in
# #     meta={'foo': 'bar'}  # Arbitrary pickleable data on the job itself
# # )
