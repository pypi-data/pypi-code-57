from django.contrib.auth import get_user_model
from django.db import models


# Here we're defined another model next to built-in auth.User instead
# of adding these fields to it. This is because Django does not support
# such migrating in the middle of project without hacks.
# Advices from google do not work. Advices like "purge all migrations
# in the project and create them again" are bad.
# https://code.djangoproject.com/ticket/25313
# https://stackoverflow.com/questions/47059198/lazy-reference-doesnt-provide-model-user
class UserDetails(models.Model):
    user = models.OneToOneField(get_user_model(), None, primary_key=True)
    comment = models.TextField(null=True, blank=True)
