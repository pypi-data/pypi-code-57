from django.db import models

from remo_app.remo.api.constants import JobStatus, JobType
from .dataset import Dataset


class Job(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    info = models.TextField()
    dataset = models.ForeignKey(Dataset, models.CASCADE, related_name='jobs', null=True)
    status = models.CharField(max_length=255,
                              choices=JobStatus.choices(),
                              default=JobStatus.unknown.name)
    job_type = models.CharField(max_length=255,
                                choices=JobType.choices(),
                                default=JobType.unknown.name)

    class Meta:
        ordering = ['-created_at']
        db_table = 'jobs'

    @staticmethod
    def update_status(job_id, status):
        job = Job.objects.get(pk=job_id)
        job.status = status
        job.save()
