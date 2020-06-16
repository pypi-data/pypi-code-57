from datetime import timezone

from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from boto3 import Session


def create_refreshing_session(
    dli_client_session, **kwargs
):
    """
    :param dli_client_session: We must not be closing over the original
    variable in a multi-threaded env as the state can become shared.
    :param kwargs:
    :return:
    """

    def refresh():
        auth_key = dli_client_session.auth_key
        expiry_time = dli_client_session.token_expires_on.replace(
            tzinfo=timezone.utc
        ).isoformat()

        return dict(
            access_key=auth_key,
            secret_key='noop',
            token='noop',
            expiry_time=expiry_time,
        )

    _refresh_meta = refresh()

    session_credentials = RefreshableCredentials.create_from_metadata(
        metadata=_refresh_meta,
        refresh_using=refresh,
        method='noop'
    )

    session = get_session()
    session._credentials = session_credentials
    return Session(
        botocore_session=session,
        **kwargs
    )
