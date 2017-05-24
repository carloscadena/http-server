# -*- coding: utf-8 -*-
"""Test for the client server pair for echo."""
from __future__ import unicode_literals
import pytest


SERVER_PARAMS_TABLE = [
    ('Hello', 'Hello'),
    ('hello my name is chris and i am in python 401',
     'hello my name is chris and i am in python 401'),
    ('12345678', '12345678'),
    ('1234567890123456', '1234567890123456'),
    ('««««', '««««')
]


@pytest.mark.parametrize('message, result', SERVER_PARAMS_TABLE)
def test_client_server_echo(message, result):
    """Test message send and recieve."""
    from client import client
    assert client(message) == result
