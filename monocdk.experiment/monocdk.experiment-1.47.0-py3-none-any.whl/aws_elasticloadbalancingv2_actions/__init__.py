import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Duration as _Duration_5170c158)
from ..aws_cognito import (IUserPool as _IUserPool_e9547b0f, IUserPoolClient as _IUserPoolClient_fd99c9a8, IUserPoolDomain as _IUserPoolDomain_a6fbdcfa)
from ..aws_elasticloadbalancingv2 import (ListenerAction as _ListenerAction_941cc841, UnauthenticatedAction as _UnauthenticatedAction_217b7279)


class AuthenticateCognitoAction(_ListenerAction_941cc841, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_elasticloadbalancingv2_actions.AuthenticateCognitoAction"):
    """A Listener Action to authenticate with Cognito.

    stability
    :stability: experimental
    """
    def __init__(self, *, next: _ListenerAction_941cc841, user_pool: _IUserPool_e9547b0f, user_pool_client: _IUserPoolClient_fd99c9a8, user_pool_domain: _IUserPoolDomain_a6fbdcfa, authentication_request_extra_params: typing.Optional[typing.Mapping[str, str]]=None, on_unauthenticated_request: typing.Optional[_UnauthenticatedAction_217b7279]=None, scope: typing.Optional[str]=None, session_cookie_name: typing.Optional[str]=None, session_timeout: typing.Optional[_Duration_5170c158]=None) -> None:
        """Authenticate using an identity provide (IdP) that is compliant with OpenID Connect (OIDC).

        :param next: What action to execute next. Multiple actions form a linked chain; the chain must always terminate in a (weighted)forward, fixedResponse or redirect action.
        :param user_pool: The Amazon Cognito user pool.
        :param user_pool_client: The Amazon Cognito user pool client.
        :param user_pool_domain: The domain prefix or fully-qualified domain name of the Amazon Cognito user pool.
        :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint. Default: - No extra parameters
        :param on_unauthenticated_request: The behavior if the user is not authenticated. Default: UnauthenticatedAction.AUTHENTICATE
        :param scope: The set of user claims to be requested from the IdP. To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP. Default: "openid"
        :param session_cookie_name: The name of the cookie used to maintain session information. Default: "AWSELBAuthSessionCookie"
        :param session_timeout: The maximum duration of the authentication session. Default: Duration.days(7)

        stability
        :stability: experimental
        """
        options = AuthenticateCognitoActionProps(next=next, user_pool=user_pool, user_pool_client=user_pool_client, user_pool_domain=user_pool_domain, authentication_request_extra_params=authentication_request_extra_params, on_unauthenticated_request=on_unauthenticated_request, scope=scope, session_cookie_name=session_cookie_name, session_timeout=session_timeout)

        jsii.create(AuthenticateCognitoAction, self, [options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_elasticloadbalancingv2_actions.AuthenticateCognitoActionProps", jsii_struct_bases=[], name_mapping={'next': 'next', 'user_pool': 'userPool', 'user_pool_client': 'userPoolClient', 'user_pool_domain': 'userPoolDomain', 'authentication_request_extra_params': 'authenticationRequestExtraParams', 'on_unauthenticated_request': 'onUnauthenticatedRequest', 'scope': 'scope', 'session_cookie_name': 'sessionCookieName', 'session_timeout': 'sessionTimeout'})
class AuthenticateCognitoActionProps():
    def __init__(self, *, next: _ListenerAction_941cc841, user_pool: _IUserPool_e9547b0f, user_pool_client: _IUserPoolClient_fd99c9a8, user_pool_domain: _IUserPoolDomain_a6fbdcfa, authentication_request_extra_params: typing.Optional[typing.Mapping[str, str]]=None, on_unauthenticated_request: typing.Optional[_UnauthenticatedAction_217b7279]=None, scope: typing.Optional[str]=None, session_cookie_name: typing.Optional[str]=None, session_timeout: typing.Optional[_Duration_5170c158]=None) -> None:
        """Properties for AuthenticateCognitoAction.

        :param next: What action to execute next. Multiple actions form a linked chain; the chain must always terminate in a (weighted)forward, fixedResponse or redirect action.
        :param user_pool: The Amazon Cognito user pool.
        :param user_pool_client: The Amazon Cognito user pool client.
        :param user_pool_domain: The domain prefix or fully-qualified domain name of the Amazon Cognito user pool.
        :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint. Default: - No extra parameters
        :param on_unauthenticated_request: The behavior if the user is not authenticated. Default: UnauthenticatedAction.AUTHENTICATE
        :param scope: The set of user claims to be requested from the IdP. To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP. Default: "openid"
        :param session_cookie_name: The name of the cookie used to maintain session information. Default: "AWSELBAuthSessionCookie"
        :param session_timeout: The maximum duration of the authentication session. Default: Duration.days(7)

        stability
        :stability: experimental
        """
        self._values = {
            'next': next,
            'user_pool': user_pool,
            'user_pool_client': user_pool_client,
            'user_pool_domain': user_pool_domain,
        }
        if authentication_request_extra_params is not None: self._values["authentication_request_extra_params"] = authentication_request_extra_params
        if on_unauthenticated_request is not None: self._values["on_unauthenticated_request"] = on_unauthenticated_request
        if scope is not None: self._values["scope"] = scope
        if session_cookie_name is not None: self._values["session_cookie_name"] = session_cookie_name
        if session_timeout is not None: self._values["session_timeout"] = session_timeout

    @builtins.property
    def next(self) -> _ListenerAction_941cc841:
        """What action to execute next.

        Multiple actions form a linked chain; the chain must always terminate in a
        (weighted)forward, fixedResponse or redirect action.

        stability
        :stability: experimental
        """
        return self._values.get('next')

    @builtins.property
    def user_pool(self) -> _IUserPool_e9547b0f:
        """The Amazon Cognito user pool.

        stability
        :stability: experimental
        """
        return self._values.get('user_pool')

    @builtins.property
    def user_pool_client(self) -> _IUserPoolClient_fd99c9a8:
        """The Amazon Cognito user pool client.

        stability
        :stability: experimental
        """
        return self._values.get('user_pool_client')

    @builtins.property
    def user_pool_domain(self) -> _IUserPoolDomain_a6fbdcfa:
        """The domain prefix or fully-qualified domain name of the Amazon Cognito user pool.

        stability
        :stability: experimental
        """
        return self._values.get('user_pool_domain')

    @builtins.property
    def authentication_request_extra_params(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The query parameters (up to 10) to include in the redirect request to the authorization endpoint.

        default
        :default: - No extra parameters

        stability
        :stability: experimental
        """
        return self._values.get('authentication_request_extra_params')

    @builtins.property
    def on_unauthenticated_request(self) -> typing.Optional[_UnauthenticatedAction_217b7279]:
        """The behavior if the user is not authenticated.

        default
        :default: UnauthenticatedAction.AUTHENTICATE

        stability
        :stability: experimental
        """
        return self._values.get('on_unauthenticated_request')

    @builtins.property
    def scope(self) -> typing.Optional[str]:
        """The set of user claims to be requested from the IdP.

        To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.

        default
        :default: "openid"

        stability
        :stability: experimental
        """
        return self._values.get('scope')

    @builtins.property
    def session_cookie_name(self) -> typing.Optional[str]:
        """The name of the cookie used to maintain session information.

        default
        :default: "AWSELBAuthSessionCookie"

        stability
        :stability: experimental
        """
        return self._values.get('session_cookie_name')

    @builtins.property
    def session_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum duration of the authentication session.

        default
        :default: Duration.days(7)

        stability
        :stability: experimental
        """
        return self._values.get('session_timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AuthenticateCognitoActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "AuthenticateCognitoAction",
    "AuthenticateCognitoActionProps",
]

publication.publish()
