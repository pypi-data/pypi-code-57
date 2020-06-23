"""Application specific configuration.  This gets overriden by the user
   to specify the registry coordinates on GCP.
"""

from django.apps import AppConfig


class GCPIoTDeviceConfig(AppConfig):
    """Users of this app will override this class and specify their
       registry coordinates.
    """
    name = 'dj_gcp_iotdevice'
    verbose_name = 'IoT Device Manager'

    # Set the following values
    project = 'GCP project id for device registry'
    location = 'GCP project location for device registry - ie us-central1'
    registry = 'GCP device registry id'
