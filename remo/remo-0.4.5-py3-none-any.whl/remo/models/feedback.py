from django.conf import settings
from django.db import models


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    text = models.TextField()
    page_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    debug_info = models.TextField(null=True, blank=True)
    screenshot = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'feedbacks'

    def __str__(self):
        return '{} | {}'.format(self.user.username,
                                self.created_at)
