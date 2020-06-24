"""Used to give the ability to add fine grained permissions to API.
"""

# pylint:disable=too-few-public-methods

from django.db import models

class GCPIotDevicePermissions(models.Model):
    """Basic model used to add fine grained permissions to API.
    """
    class Meta:
        """Only used for permissions.
        """
        managed = False  # No database table creation or deletion
                         # operations will be performed for this model.
