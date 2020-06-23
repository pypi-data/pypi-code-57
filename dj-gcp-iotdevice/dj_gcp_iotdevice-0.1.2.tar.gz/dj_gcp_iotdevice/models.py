from django.db import models

class GCPIotDevicePermissions(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion
                         # operations will be performed for this model.