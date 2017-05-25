# -*- coding: utf-8 -*-
"""Test for the client server pair for echo."""
from __future__ import unicode_literals
import pytest


SERVER_OK_PARAMS = [
    ('Hello', 'HTTP/1.1 200 OK\r\n'),
    ('hello my name is chris and i am in python 401',
     'HTTP/1.1 200 OK\r\n'),
    ('12345678',
     'HTTP/1.1 200 OK\r\n'),
]


ERORR_PARAMS = [
    (b'HTTP/1.1 500 Internal Server Error\r\n\r\n')
]


OK_PARAMS = [
    (b'HTTP/1.1 200 OK\r\n')
]


@pytest.mark.parametrize('message, result', SERVER_OK_PARAMS)
def test_client_server_response_ok(message, result):
    """Test message send and recieve."""
    from client import client
    message = client(message)
    message = message[0:-39]
    assert message == result


@pytest.mark.parametrize('result', ERORR_PARAMS)
def test_response_error(result):
    """Test message send and recieve."""
    from server import response_error
    assert response_error() == result


@pytest.mark.parametrize('result', OK_PARAMS)
def test_response_ok(result):
    """Test message send and recieve."""
    from server import response_ok
    msg = response_ok()
    msg = msg[0:-39]
    assert msg == result
