"""Main set of views provided by the application

  :raises NotFound: Specified a device that does not exist.
  :raises ParseError: Invalid data provided - likely a bad public key.
  :raises NotAcceptable: Operation was rejects - maybe creating a device that already exists.
  :raises PermissionDenied: Likely bad registry coordinates or enough GCP permissions have
                            not been given to manage the registry.
"""

from typing import List, Dict, cast
from google.api_core.exceptions import (
    NotFound as GCPNotFound,
    AlreadyExists,
    InvalidArgument,
    PermissionDenied as GCPPermissionDenied
)
from google.cloud import iot_v1
from rest_framework.exceptions import (
    NotFound,
    NotAcceptable,
    ParseError,
    PermissionDenied
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from django.apps import apps

from .serializers import DeviceSerializer
from .apps import GCPIoTDeviceConfig


class DevicesViewset(GenericViewSet):
    """Provides a CRDL (Create, Retrieve, Delete, List) interface to GCP IoT Core.

    :raises NotFound: Specified a device that does not exist.
    :raises ParseError: Invalid data provided - likely a bad public key.
    :raises NotAcceptable: Operation was rejects - maybe creating a device that already exists.
    :raises PermissionDenied: Likely bad registry coordinates or enough GCP permissions have
                              not been given to manage the registry.
    """
    serializer_class = DeviceSerializer

    @property
    def client(self):
        """IoT Client to access the GCP IoT APIs

        :return: Client that can be used to access the GCP IoT API
        :rtype: Client
        """
        return iot_v1.DeviceManagerClient()

    @property
    def config(self) -> GCPIoTDeviceConfig:
        """Used to return the overridden app configuration that specifies the registry coordinates.

        :return: Application configuration
        :rtype: GCPIoTDeviceConfig
        """
        return cast(GCPIoTDeviceConfig, apps.get_app_config('dj_gcp_iotdevice'))

    @property
    def registry_path(self) -> str:
        """Returns the fully qualified path to the registry.

        :return: Fully qualified path to the registry.
        :rtype: str
        """
        return self.client.registry_path(self.config.project, self.config.location,
                                         self.config.registry)

    @property
    def device_path(self) -> str:
        """Returns the fully qualified path to access an IoT device.

        :return: Fully qualified path to access the device.
        :rtype: str
        """
        device_id = self.kwargs[self.lookup_url_kwarg]
        return self.client.device_path(self.config.project, self.config.location,
                                       self.config.registry, device_id)

    def get_queryset(self) -> List[Dict[str, str]]:
        """Returns an iterator that can be used to access the list of devices.

        :return: List of devices in the registry.
        :rtype: List[Dict[str, str]]
        """
        return self.client.list_devices(self.registry_path)

    def get_object(self) -> Dict[str, str]:
        """Returns a specific IoT device.

        :raises NotFound: Raised if the device does not exist.
        :return: Device
        :rtype: Dict[str, str]
        """
        try:
            device = self.client.get_device(self.device_path)
        except GCPNotFound:
            raise NotFound

        return {
            'id': device.id,
            'public_key': device.credentials[0].public_key.key
        }

  #######################################
  # Implementation of CRDL interface.
  #######################################

    def create(self, request, *_args, **_kwargs):
        """Used to add a new IoT device to the registry.

        :raises ParseError: Bad data provided.  Likely a bad public key.
        :raises NotAcceptable: Could not add device.  Probably device Id already exists.
        :raises PermissionDenied: Likely wrong GCP coordinates or insufficient permissions
                                  on GCP to add devices to the registry.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_template = {
            'id': serializer.data['id'],
            'credentials': [{
                'public_key': {
                    'format': 'RSA_PEM',
                    'key': serializer.data['public_key']
                }
            }]
        }
        try:
            self.client.create_device(self.registry_path, device_template)
        except InvalidArgument as exc:
            raise ParseError(exc.message)
        except AlreadyExists as exc:
            raise NotAcceptable(exc.message)
        except GCPPermissionDenied as exc:
            raise PermissionDenied(f'{exc.message} - Is your project, location, and '
                                   'registry setup correctly?')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, _request, *_args, **_kwargs):
        """Used to get one device from the registry.

        :raises PermissionDenied: Likely bad coordinates to registry or not enough
                                  permissions to read devices from registry.
        :raises NotFound: Device does not exist.
        """
        try:
            response = Response(self.get_serializer(self.get_object()).data)
        except GCPPermissionDenied as exc:
            raise PermissionDenied(f'{exc.message} - Is your project, location, and '
                                   'registry setup correctly?')
        return response

    def destroy(self, _request, *_args, **_kwargs):
        """Used to remove a device from the registry.

        :raises PermissionDenied: Likely bad coordinates to registry or not enough
                                  permissions to remove devices from the registry.
        :raises NotFound: Device does not exist.
        """
        try:
            self.client.delete_device(self.device_path)
        except GCPPermissionDenied as exc:
            raise PermissionDenied(f'{exc.message} - Is your project, location, and '
                                   'registry setup correctly?')
        except GCPNotFound:
            pass # Gracefully handle since it is already deleted

        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, _request, *_args, **_kwargs):
        """Used to list all the devices in the registry.

        :raises PermissionDenied: Likely bad coordinates to registry or not enough permissions
                                  to list devices from registry.
        """
        try:
            response = Response(self.get_serializer(self.get_queryset(), many=True).data)
        except GCPPermissionDenied as exc:
            raise PermissionDenied(f'{exc.message} - Is your project, location, and registry '
                                   'setup correctly?')
        return response
