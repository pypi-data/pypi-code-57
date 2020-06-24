#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 22.06.20
@author: eisenmenger
"""
import pytest

from unittest import mock
from unittest.mock import call
from kombunicator.tasks import _rpc_server_publisher


@pytest.fixture(scope='module')
def conn_param():
    return {
        'hostname': '127.0.0.1',
        'port': '6397',
        'userid': 'jondoe',
        'password': 'superstrong_password',
    }


@mock.patch('kombunicator.tasks.MessageProducer')
def test_rpc_server_publisher_task(mocked_msg_prod, conn_param):
    def _test_message_producer_init():
        _rpc_server_publisher(message='Some message',
                              connection_parameter=conn_param,
                              routing_key='rpc_server_key',
                              correlation_id='service')

        mocked_msg_prod.assert_called_with(conn_param)
        assert mocked_msg_prod.called
        assert mocked_msg_prod.called_once

    def _test_message_producer_publish_called():
        _rpc_server_publisher(message='Some other message',
                              connection_parameter=conn_param,
                              routing_key='rpc_server_key',
                              correlation_id='operation')

        expected_call = call().publish(message='Some other message',
                                       routing_key='rpc_server_key',
                                       correlation_id='operation')
        assert mocked_msg_prod.mock_calls[-1] == expected_call

    _test_message_producer_init()
    _test_message_producer_publish_called()
