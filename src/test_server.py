# -*- coding: utf-8 -*-
"""Test for the client server pair for echo."""
from __future__ import unicode_literals
import pytest


SERVER_PARAMS_TABLE = [
    ('Hello', 'HTTP/1.1 200 OK\r\nMessage recieved.'),
    ('hello my name is chris and i am in python 401',
     'HTTP/1.1 200 OK\r\nMessage recieved.'),
    ('12345678', 'HTTP/1.1 200 OK\r\nMessage recieved.'),
]


@pytest.mark.parametrize('message, result', SERVER_PARAMS_TABLE)
def test_client_server_echo(message, result):
    """Test message send and recieve."""
    from client import client
    assert client(message) == result
