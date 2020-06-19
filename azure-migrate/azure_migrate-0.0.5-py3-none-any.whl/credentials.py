from azure.common.credentials import ServicePrincipalCredentials
from msrestazure.azure_exceptions import CloudError
import os

try:
    class CredentialsAzure:
        """Class to get Azure credential from service principal

            Needs three variables of environments:

            - CLIENT_ID
            - SECRET
            - TENANT

            Two methods how property:

            :property get_credentials_sp: return type credentials Azure.
            :property get_token_sp: return type string token.
            
        """

        def __init__(self):
            pass

        @property    
        def get_credentials_sp(self):

            __credentials = ServicePrincipalCredentials(
                client_id=os.environ["CLIENT_ID"],
                secret=os.environ["SECRET"],
                tenant=os.environ["TENANT"]
            )

            return __credentials
        
        @property
        def get_token_sp(self):

            __credentials = ServicePrincipalCredentials(
                client_id=os.environ["CLIENT_ID"],
                secret=os.environ["SECRET"],
                tenant=os.environ["TENANT"]
            )

            return __credentials.token["access_token"]

except (TimeoutError, EOFError, ValueError, CloudError) as err:
    raise err