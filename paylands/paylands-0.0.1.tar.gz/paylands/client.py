from enum import Enum
from typing import Any, Optional

from paylands.exceptions import handle_error_response
from paylands.session import APISession


class OrderOperative(Enum):
    AUTHORIZATION = 'AUTHORIZATION'
    DEFERRED = 'DEFERRED'
    PAYOUT = 'PAYOUT'
    TRANSFER = 'TRANSFER'


class PlanIntervalType(Enum):
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    YEARLY = 'YEARLY'


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Paylands(object):
    def __init__(self, api_key: str, signature: str, service: str,
                 url: Optional[str] = None):
        self.api_key = api_key
        self.signature = signature
        self.service = service
        self.url = url or 'https://api.paylands.com/v1'

        # Initialize the session.
        self.session = APISession()
        self.session.init_auth(self.api_key)

    # Perform an API request.
    def _request(self, endpoint: str, method: HttpMethod, params=None):

        url = f'{self.url}/{endpoint}'
        resp = self.session.request(method.value, url, json=params)

        # If something goes wrong, we'll pass the response
        # off to the error-handling code
        if resp.status_code >= 400:
            handle_error_response(resp)

        # Otherwise return the result dictionary.
        return resp.json()

    # API methods

    def generate_order(self,
                       amount: int,
                       description: str,
                       operative: OrderOperative,
                       customer_ext_id: Optional[str] = None,
                       additional: Optional[str] = None,
                       url_post: Optional[str] = None,
                       url_ok: Optional[str] = None,
                       url_ko: Optional[str] = None,
                       template_uuid: Optional[str] = None,
                       dcc_template_uuid: Optional[str] = None,
                       source_uuid: Optional[str] = None,
                       extra_data: Optional[Any] = None,
                       secure: bool = True):

        # Ensuring that is a enum value
        operative = OrderOperative(operative)

        params = {
            'signature': self.signature,
            'service': self.service,

            'amount': amount,
            'description': description,
            'operative': operative.value,
            'secure': secure,
        }

        if customer_ext_id:
            params.update({'customer_ext_id': customer_ext_id})

        if additional:
            params.update({'additional': additional})

        if url_post:
            params.update({'url_post': url_post})

        if url_ok:
            params.update({'url_ok': url_ok})

        if url_ko:
            params.update({'url_ko': url_ko})

        if template_uuid:
            params.update({'template_uuid': template_uuid})

        if dcc_template_uuid:
            params.update({'dcc_template_uuid': dcc_template_uuid})

        if source_uuid:
            params.update({'source_uuid': source_uuid})

        if extra_data:
            params.update({'extra_data': extra_data})

        return self._request('payment', HttpMethod.POST, params)

    def make_direct_payment(self,
                            order_uuid: str,
                            card_uuid: str,
                            customer_ip: str = None):
        params = {
            'signature': self.signature,
            'order_uuid': order_uuid,
            'card_uuid': card_uuid,
        }

        if customer_ip:
            params.update({'customer_ip': customer_ip})

        return self._request('payment/direct', HttpMethod.POST, params)

    def save_credit_card(self,
                         customer_ext_id: str,
                         card_holder: str,
                         card_pan: str,
                         card_expiry_year: str,
                         card_expiry_month: str,
                         card_cvv: str = None,
                         additional: str = None,
                         url_post: str = None,
                         validate: bool = True):
        params = {
            'signature': self.signature,
            'service': self.service,

            'customer_ext_id': customer_ext_id,
            'card_holder': card_holder,
            'card_pan': card_pan,
            'card_expiry_year': card_expiry_year,
            'card_expiry_month': card_expiry_month,
        }

        if card_cvv:
            params.update({'card_cvv': card_cvv})
        if additional:
            params.update({'additional': additional})
        if url_post:
            params.update({'url_post': url_post})
        if validate:
            params.update({'validate': validate})

        return self._request('payment-method/card', HttpMethod.POST, params)

    def create_company(self):
        params = {
            'signature': self.signature,
        }

        return self._request('subscriptions/company', HttpMethod.POST, params)

    def get_company(self):
        return self._request('subscriptions/company', HttpMethod.GET)

    def create_customer(self, external_id: str):

        params = {
            'signature': self.signature,

            'customer_ext_id': external_id,
        }

        return self._request('customer', HttpMethod.POST, params)

    def get_customer(self, external_id: str):

        params = {
            'signature': self.signature,

            'customer_ext_id': external_id,
        }

        return self._request('customer', HttpMethod.GET, params)

    def create_profile(self,
                       external_id: str,
                       first_name: str,
                       last_name: str,
                       cardholder_name: str = None,
                       document_identification_issuer_type=None,
                       document_identification_type=None,
                       document_identification_number: str = None,
                       email: str = None,
                       phone=None,
                       home_phone=None,
                       work_phone=None,
                       mobile_phone=None,
                       birthdate: str = None,
                       source_of_funds: str = None,
                       occupation: str = None,
                       social_security_number: str = None):

        params = {
            'signature': self.signature,

            'external_id': external_id,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'home_phone': home_phone,
            'work_phone': work_phone,
            'mobile_phone': mobile_phone,
        }

        if cardholder_name:
            params.update({'cardholder_name': cardholder_name})
        if document_identification_issuer_type:
            params.update({'document_identification_issuer_type':
                           document_identification_issuer_type})
        if document_identification_type:
            params.update({'document_identification_type':
                           document_identification_type})
        if document_identification_number:
            params.update({'document_identification_number':
                           document_identification_number})
        if email:
            params.update({'email': email})
        if birthdate:
            params.update({'birthdate': birthdate})
        if source_of_funds:
            params.update({'source_of_funds': source_of_funds})
        if occupation:
            params.update({'occupation': occupation})
        if social_security_number:
            params.update({'social_security_number': social_security_number})

        return self._request('customer/profile', HttpMethod.POST, params)

    def update_profile(self,
                       external_id: str,
                       first_name: str,
                       last_name: str,
                       cardholder_name: str = None,
                       document_identification_issuer_type=None,
                       document_identification_type=None,
                       document_identification_number: str = None,
                       email: str = None,
                       phone=None,
                       home_phone=None,
                       work_phone=None,
                       mobile_phone=None,
                       birthdate: str = None,
                       source_of_funds: str = None,
                       occupation: str = None,
                       social_security_number: str = None):

        params = {
            'signature': self.signature,

            'external_id': external_id,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'home_phone': home_phone,
            'work_phone': work_phone,
            'mobile_phone': mobile_phone,
        }

        if cardholder_name:
            params.update({'cardholder_name': cardholder_name})
        if document_identification_issuer_type:
            params.update({'document_identification_issuer_type':
                           document_identification_issuer_type})
        if document_identification_type:
            params.update({'document_identification_type':
                           document_identification_type})
        if document_identification_number:
            params.update({'document_identification_number':
                           document_identification_number})
        if email:
            params.update({'email': email})
        if birthdate:
            params.update({'birthdate': birthdate})
        if source_of_funds:
            params.update({'source_of_funds': source_of_funds})
        if occupation:
            params.update({'occupation': occupation})
        if social_security_number:
            params.update({'social_security_number': social_security_number})

        return self._request('customer/profile', HttpMethod.PUT, params)

    def get_profile(self, external_id: str):

        params = {
            'signature': self.signature,
        }

        return self._request(
            f'customer/profile/{external_id}', HttpMethod.GET, params)

    def create_plan(self,
                    name: str,
                    external_id: str,
                    product: str,
                    amount: int,
                    interval: int,
                    interval_type: PlanIntervalType,
                    trial_available: Optional[bool] = None,
                    interval_offset: Optional[int] = None,
                    interval_offset_type: Optional[PlanIntervalType] = None):

        interval_type = PlanIntervalType(interval_type)

        params = {
            'signature': self.signature,

            'name': name,
            'external_id': external_id,
            'product': product,
            'amount': amount,
            'interval': interval,
            'interval_type': interval_type.value,
        }

        if trial_available:
            params.update({'trial_available': trial_available})

        if interval_offset:
            params.update({'interval_offset': interval_offset})

        if interval_offset_type:
            interval_offset_type = PlanIntervalType(interval_offset_type)
            params.update({'interval_offset_type': interval_offset_type.value})

        return self._request('subscriptions/plan', HttpMethod.POST, params)

    def get_plan(self, external_id: str):
        return self._request(
            f'subscriptions/plan/{external_id}', HttpMethod.GET)

    def create_product(self,
                       name: str,
                       external_id: str,
                       notification_url: Optional[str] = None):

        params = {
            'signature': self.signature,

            'name': name,
            'external_id': external_id,
        }

        if notification_url:
            params.update({'notification_url': notification_url})

        return self._request('subscriptions/product', HttpMethod.POST, params)

    def get_product(self, external_id: str):
        return self._request(
            f'subscriptions/product/{external_id}', HttpMethod.GET)


# {
#     "signature": "121149a0ba5361191d740fa898784a8b",
#     "amount": 400,
#     "operative": "AUTHORIZATION",
#     "customer_ext_id": "user1024",
#     "additional": "usuario1234",
#     "service": "60A1F4C0-CC58-47A9-A0B9-868F9EF29045",
#     "secure": true,
#     "url_post": "https://mysite.com/payment/result",
#     "url_ok": "https://mysite.com/payment/success",
#     "url_ko": "https://mysite.com/payment/error",
#     "template_uuid": "6a93c26e-954d-47ea-83bf-21fa29b68f28",
#     "dcc_template_uuid": "ea0d5f53-5901-4c6b-9d4a-7e7c9b0eeb7e",
#     "description": "order's description",
#     "source_uuid": "2b0600286a8f41479c22968f568c9738",
#     "extra_data": {
#         "profile": {
#             "first_name": "Saville J",
#             "last_name": "Dulce Armentrout",
#             "cardholder": "Saville J Dulce Armentrout",
#             "document_identification_issuer_type: `FEDERAL_GOVERMENT`":
# "STATE_GOVERNMENT",
#             "document_identification_type": "NATIONAL_IDENTITY_DOCUMENT",
#             "document_identification_number": "12345678Z",
#             "phone": {
#               "number": "654123789",
#               "prefix": "123"
#             },
#             "home_phone": {
#                 "number": "654123789",
#                 "prefix": "123"
#             },
#             "work_phone": {
#                 "number": "654123789",
#                 "prefix": "123"
#             },
#             "mobile_phone": {
#                 "number": "654123789",
#                 "prefix": "123"
#             },
#             "birth_date": "1971-08-05",
#             "source_of_funds": "Salary",
#             "occupation": "Shoe Machine Operators",
#             "social_security_number": "503-33-4388",
#             "address": {
#                 "address1": "Ronda",
#                 "address2": "Magdalena",
#                 "address3": "número 20",
#                 "city": "Castellón",
#                 "state_code": "Castellón",
#                 "country": "ESP",
#                 "zip_code": "12006"
#             },
#             "billing_address": {
#                 "address1": "Ronda",
#                 "address2": "Magdalena",
#                 "address3": "número 20",
#                 "city": "Castellón",
#                 "state_code": "Castellón",
#                 "country": "ESP",
#                 "zip_code": "12006"
#             },
#             "shipping_address": {
#                 "address1": "Ronda",
#                 "address2": "Magdalena",
#                 "address3": "número 20",
#                 "city": "Castellón",
#                 "state_code": "Castellón",
#                 "country": "ESP",
#                 "zip_code": "12006"
#             }
#         },
#         "payment": {
#             "installments": 3
#         },
#         "cof": {
#             "is_initial": false,
#             "reason": "INSTALLMENTS",
#             "first_payment_uuid": "6BFF5C76-31FC-4257-9A56-3DBE898989C9"
#         },
#         "halcash": {
#             "sender_name": "Patricio",
#             "secret_key": "4321",
#             "expiry_date": "2020-04-18"
#         }
#     }
# }


class PaylandsSandbox(Paylands):
    def __init__(self, api_key: str, signature: str, service: str,
                 url: Optional[str] = None):
        url = url or 'https://api.paylands.com/v1/sandbox'
        super().__init__(api_key, signature, service, url)
