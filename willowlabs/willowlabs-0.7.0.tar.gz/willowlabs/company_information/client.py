import os
import json
import grpc
from time import time
from datetime import date
from google.protobuf.json_format import MessageToDict
from willowlabs.tools import tools, protobuffer_tools as pb_tools
from willowlabs.service_grpc.company_information import company_information_service_pb2 as pb2, \
    company_information_service_pb2_grpc as pb2_grpc
from typing import Any, Optional, Union
from functools import wraps


def _check_jwt(f):
    @wraps(f)
    def wrapped_function(self, *args, **kwargs):
        if self.jwt is None or self.jwt_expires is None or self.jwt_expires < time():
            self.get_json_web_token()
        return f(self, *args, **kwargs)
    return wrapped_function


class CompanyInformationClient:
    """
    Class to access Willow Labs API.
    """

    def __init__(self, configuration_path: str, **kwargs: Any):
        """
        Initialize the client.
        Args:
            configuration_path: The path of the configuration file.
            **kwargs: Extra arguments.
        """
        self.configuration_path = configuration_path
        self.configuration = None
        self.service_type = kwargs.get("service_type", "production")
        self.credentials_info = None
        self.host = None
        self.issuer = None
        self.audiences = None
        self.jwt = None
        self.jwt_expires = None
        self.api_key = None
        self.timeout = kwargs.get("timeout", 120)        # Seconds
        self.scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        self.return_dict = kwargs.get("return_dict", False)

    def load_configuration(self):
        """
        Loads the configuration into memory.
        """
        self.configuration = tools.load_client_configuration(self.configuration_path)
        self.host = self.configuration["service"][self.service_type]["host"]
        self.issuer = self.configuration["service"][self.service_type]["authentication"]["issuer"]
        self.audiences = self.configuration["service"][self.service_type]["authentication"]["audiences"]
        self.api_key = self.configuration["service"][self.service_type]["api_key"]

    def load_credentials(self):
        """
        Loads the credentials into memory.
        """
        if self.configuration is None:
            self.load_configuration()
        configuration = self.configuration["service"][self.service_type]
        path = configuration["service_account_credentials"]
        if path.endswith(".json") and os.path.exists(path):
            with open(path, "r") as fp:
                self.credentials_info = json.load(fp)
        else:
            raise FileNotFoundError(f"Unable to find credentials in path {path}.")

    def get_json_web_token(self):
        """
        Loads the web token into memory Uses impersonation of Willowlabs service account by currently signed in service account.
        This will enable the current service account to behave as if it was logged in as Willow Labs API service account. Billing for billable requests to gcloud will be billed to current service account.
        """
        if self.credentials_info is None:
            self.load_credentials()
        token, expires = tools.generate_jwt_token_from_impersonated_account(self.credentials_info, self.audiences,
                                                                            self.issuer)
        self.jwt = token
        self.jwt_expires = expires

    @_check_jwt
    def get_company_ownership(self, organisation_number: int, record_year: int, depth: int = 25, cutoff: float = 1.0,
                              top: int = 0) -> pb2.OwnershipResponse:
        """
        Get owners for a company.
        Args:
            organisation_number: The organization number for the company being queried.
            record_year: The ownership year.
            depth: Max depth of ownership structure returned.
            cutoff: Minimum percentage of ownership for inclusion in result.
            top: The number of max elements returned (The top N owners).
        Returns:
            The ownership structure.
        """
        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.OwnershipRequest(organisation_number=organisation_number, record_year=record_year,
                                           depth=depth, cutoff=cutoff, top=top)
            ownership_information = stub.get_company_ownership(request, self.timeout, metadata=metadata)
        return MessageToDict(ownership_information) if self.return_dict else ownership_information

    @_check_jwt
    def get_company_roles(self, organisation_number: int, query_date: Optional[date] = None) -> pb2.RoleResponse:
        """
        Get the roles for a company.
        Args:
            organisation_number: The organization number for the company being queried.
            query_date: Information retrieved will be the one valid at this date.

        Returns:
            The roles belonging to the given organization number.
        """
        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.RoleRequest(organisation_number=organisation_number,
                                      query_date=pb_tools.date_to_pb2_date(query_date))
            roles = stub.get_company_roles(request, self.timeout, metadata=metadata)
        return MessageToDict(roles) if self.return_dict else roles

    @_check_jwt
    def get_basic_company_information(self, organisation_number: int,
                                      query_date: Optional[date] = None) -> pb2.BasicCompanyInformationResponse:
        """
        Get the basic information for a company. May include address, industrikode (industry code), næringskode (business code).
        Args:
            organisation_number: The organization number for the company being queried.
            query_date: Information retrieved will be the one valid at this date.

        Returns:
            The the basic information of the organization number given.
        """
        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.BasicCompanyInformationRequest(organisation_number=organisation_number,
                                                         query_date=pb_tools.date_to_pb2_date(query_date))
            results = stub.get_basic_company_information(request, self.timeout, metadata=metadata)
        return MessageToDict(results) if self.return_dict else results

    @_check_jwt
    def _get_company_signatory_information(self, organisation_number: int,
                                           authority_type: Union[str, int],
                                           query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        """
        Get the authority holders for the company for a given authority type.
        Args:
            organisation_number: The organization number for the company being queried.
            authority_type: The authority type being requested.
            query_date: Information retrieved will be the one valid at this date.

        Returns:
            The signature holders of the given organization number.
        """
        if isinstance(authority_type, str):
            try:
                authority_type = getattr(pb2.SignatoryAuthorityTypes, authority_type.upper())
            except AttributeError:
                raise ValueError(f"Unknown authority type '{authority_type}'. Authority type must be among "
                                 f"'POWER_OF_ATTORNEY', 'PROKURA', 'FULL_SIGNATORY_AUTHORITY', or 'SIGNATUR'.")

        if authority_type == pb2.SignatoryAuthorityTypes.UNKNOWN_AUTHORITY:
            raise ValueError(f"Authority type may not be UNKNOWN_AUTHORITY.")

        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.SignatoryInformationRequest(organisation_number=organisation_number,
                                                      authority_type=authority_type,
                                                      query_date=pb_tools.date_to_pb2_date(query_date))
            results = stub.get_company_signatory_information(request, self.timeout, metadata=metadata)
        return MessageToDict(results) if self.return_dict else results

    @_check_jwt
    def get_company_power_of_attorney(self, organisation_number: int,
                                      query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        """
        Get the power of attorney (prokura) for the company. Power of attorney is the signature rights for all daily operations.
        See (in Norwegian): `Lovdata <https://lovdata.no/dokument/NL/lov/1985-06-21-80>`_ or `Wikipedia <https://no.wikipedia.org/wiki/Prokura>`_.

        English version of :func:`~willowlabs.company_information.client.CompanyInformationClient.get_company_prokura`.

        Args:
            organisation_number: The organization number for the company being queried.
            query_date: Information retrieved will be the one valid at this date.

        Returns:
            The list of all the the power of attorney rights.
        """
        return self._get_company_signatory_information(organisation_number,
                                                       pb2.SignatoryAuthorityTypes.POWER_OF_ATTORNEY,
                                                       query_date=query_date)

    @_check_jwt
    def get_company_full_signatory_authority(self, organisation_number: int,
                                             query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        """
        Get the signature holders for a company. Signature is the right to sign for the companies in all situations.
        Extension of prokura which is only for daily operations.

        English version of :func:`~willowlabs.company_information.client.CompanyInformationClient.get_company_signatur`.

        Args:
            organisation_number: The organization number for the company being queried.
            query_date: The date to get the signature for.

        Returns:
            The signature holders.
        """
        return self._get_company_signatory_information(organisation_number,
                                                       pb2.SignatoryAuthorityTypes.FULL_SIGNATORY_AUTHORITY,
                                                       query_date=query_date)

    @_check_jwt
    def get_company_prokura(self, organisation_number: int,
                            query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        """
        Get the prokura rights for the company. Prokura is the signature rights for all daily operations.
        See: `Lovdata <https://lovdata.no/dokument/NL/lov/1985-06-21-80>`_ or `Wikipedia <https://no.wikipedia.org/wiki/Prokura>`_.

        Norwegian version of :func:`~willowlabs.company_information.client.CompanyInformationClient.get_company_power_of_attorney`.

        Args:
            organisation_number: The organization number for the company being queried.
            query_date: Information retrieved will be the one valid at this date.

        Returns:
            The list of all prokuras.
        """
        return self._get_company_signatory_information(organisation_number,
                                                       pb2.SignatoryAuthorityTypes.PROKURA,
                                                       query_date=query_date)

    @_check_jwt
    def get_company_signatur(self, organisation_number: int,
                             query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        """
        Get the signature holders for a company. Signature is the right to sign for the companies in all situations.
        Extension of prokura which is only for daily operations.

        Norwegian version of :func:`~willowlabs.company_information.client.CompanyInformationClient.get_company_full_signatory_authority`.

        Args:
            organisation_number: The organization number for the company being queried.
            query_date: The date to get the signature for.

        Returns:
            The signature holders.
        """
        return self._get_company_signatory_information(organisation_number,
                                                       pb2.SignatoryAuthorityTypes.SIGNATUR,
                                                       query_date=query_date)
