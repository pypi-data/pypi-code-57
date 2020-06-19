# from django.conf import settings
#
# from remo_app.remo.use_cases import is_remo_local
#
# if not is_remo_local():
#     import django_rq
#
# from remo_app.remo.api.constants import JobType, JobStatus
# from remo_app.remo.models import Dataset, Job
#
#
# def enqueue_dataset_job(dataset: Dataset, job_type: JobType, job_func, *args, **kwargs):
#     job_timeout = settings.RQ.get('DEFAULT_TIMEOUT')
#     ttl = settings.RQ.get('DEFAULT_TTL')
#     result_ttl = settings.RQ.get('DEFAULT_RESULT_TTL')
#
#     job = django_rq.enqueue(job_func, *args,
#                             job_timeout=job_timeout,
#                             ttl=ttl,
#                             result_ttl=result_ttl)
#     Job.objects.create(id=job.id, dataset=dataset, status=JobStatus.queued.name,
#                        job_type=job_type.name, info=kwargs.get('info'))
#     return job
