# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Signal Client API
"""
import logging

from ._vendors.sqreen_security_signal_sdk import Client
from ._vendors.sqreen_security_signal_sdk.sender import Sender
from .config import CONFIG
from .http_client import USER_AGENT

LOGGER = logging.getLogger(__name__)


class SignalSender(Sender):

    default_base_url = CONFIG["INGESTION_URL"]


class SignalClient(Client):

    sender_class = SignalSender


def get_signal_client(session, batch_size=0, max_staleness=0,
                      user_agent=USER_AGENT):
    """ Get a Signal Client.
    """
    client = SignalClient(
        token=session.session_token,
        max_batch_size=batch_size,
        interval_batch=max_staleness,
        session_token=True,
        proxy_url=CONFIG["PROXY_URL"],
    )
    client.user_agent = session.connection.user_agent
    return client
