# -*- coding: utf-8 -*-
"""Test for the client server pair for echo."""
from __future__ import unicode_literals
from server import parse_request
from client import client
from email.utils import formatdate
import pytest

SERVER_PARSE_OK_PARAMS = [
    ('GET /index.html HTTP/1.1 Host: www.yourwebsite.com:80',
        b'/index.html'),
    ('GET smelly/stuff/index.html HTTP/1.1 Host: www.yourwebsite.com:80',
        b'smelly/stuff/index.html'),
    ('GET bleh/bleh.html HTTP/1.1 Host: www.yourwebsite.com:80',
        b'bleh/bleh.html')
]

TEST_PARSE_ERROR_CODE_400 = [
    ('GET /index.html HTTP/1.1 Hosts: www.yourwebsite.com:80'),
    ('GET smelly/stuff/index.html HTTP/1.1 Bosst: www.yourwebsite.com:80'),
    ('GET bleh/bleh.html HTTP/1.1 shmost: www.yourwebsite.com:80')
    ]

TEST_PARSE_ERROR_CODE_505 = [
    ('GET /index.html HTTPP/1.1 Hosts: www.yourwebsite.com:80'),
    ('GET smelly/stuff/index.html HTTP Bosst: www.yourwebsite.com:80'),
    ('GET bleh/bleh.html http/1.1 shmost: www.yourwebsite.com:80')
    ]

TEST_PARSE_ERROR_CODE_405 = [
    ('POST /index.html HTTPP/1.1 Hosts: www.yourwebsite.com:80'),
    ('get smelly/stuff/index.html HTTP Bosst: www.yourwebsite.com:80'),
    ('GEET bleh/bleh.html http/1.1 shmost: www.yourwebsite.com:80')
    ]

TEST_PARSE_ERROR_LEN_PARAMS = [
    ('GET /index.html HTTP/1.1 Host:'),
    ('ASDFA SDFASDF ASDFASDF ASDFADFA GASGASG ADSFA'),
    ('GET /index.html HTTP/1.1 Host: www.google.com:80 :)')
    ]

TEST_OK_PARAMS = [
    (b'HTTP/1.1 200 OK\r\n')
]

TEST_RESPONSE_ERROR_PARAMS = [
    ('400 Bad Request', b'HTTP/1.1 400 Bad Request\r\n\r\n'),
    ('505 HTTP Version Not Supported',
     b'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'),
    ('a string', b'HTTP/1.1 a string\r\n\r\n')
]

TEST_CLIENT_PARSE_OK_PARAMS = [
    ('GET /index.html HTTP/1.1 Host: www.google.com:80',
        'HTTP/1.1 200 OK\r\nDate: {}'.format(formatdate(usegmt=True))),
    ('GET /index.html HTTP/1.1 Host: www.facebook.com:80',
        'HTTP/1.1 200 OK\r\nDate: {}'.format(formatdate(usegmt=True))),
    ('GET bleh/bleh.html HTTP/1.1 Host: www.outlook.com:80',
        'HTTP/1.1 200 OK\r\nDate: {}'.format(formatdate(usegmt=True)))
]


@pytest.mark.parametrize('message, result', SERVER_PARSE_OK_PARAMS)
def test_server_parse_request_OK(message, result):
    """Test parse request function receives properly formatted request."""
    assert parse_request(message) == result


@pytest.mark.parametrize('message', TEST_PARSE_ERROR_LEN_PARAMS)
def test_parse_req_bad_len(message):
    """Test the length function in the parse request function."""
    with pytest.raises(ValueError):
        parse_request(message)


@pytest.mark.parametrize('message', TEST_PARSE_ERROR_CODE_400)
def test_parse_req_bad_host(message):
    """If host is bad, parse request function returns error code 400."""
    with pytest.raises(ValueError):
        parse_request(message)


@pytest.mark.parametrize('message', TEST_PARSE_ERROR_CODE_505)
def test_parse_req_bad_http(message):
    """If http is bad, parse request function returns error code 505."""
    with pytest.raises(ValueError):
        parse_request(message)


@pytest.mark.parametrize('message', TEST_PARSE_ERROR_CODE_405)
def test_parse_req_bad_get(message):
    """If GET is bad, parse request function returns error code 405."""
    with pytest.raises(ValueError):
        parse_request(message)


@pytest.mark.parametrize('code, result', TEST_RESPONSE_ERROR_PARAMS)
def test_response_error(code, result):
    """Test return of error message from response error function.s"""
    from server import response_error
    assert response_error(code) == result


@pytest.mark.parametrize('result', TEST_OK_PARAMS)
def test_response_ok(result):
    """Test message send and recieve."""
    from server import response_ok
    msg = response_ok()
    msg = msg[0:-39]
    assert msg == result


@pytest.mark.parametrize('message, result', TEST_CLIENT_PARSE_OK_PARAMS)
def test_server_parse_request_OK(message, result):
    """Test parse request function receives properly formatted request."""
    assert client(message) == result


# @pytest.mark.parametrize('message', TEST_PARSE_ERROR_LEN_PARAMS)
# def test_parse_req_bad_len(message):
#     """Test the length function in the parse request function."""
#     with pytest.raises(ValueError):
#         parse_request(message)
#
#
# @pytest.mark.parametrize('message', TEST_PARSE_ERROR_CODE_400)
# def test_parse_req_bad_host(message):
#     """If host is bad, parse request function returns error code 400."""
#     with pytest.raises(ValueError):
#         parse_request(message)
#
#
# @pytest.mark.parametrize('message', TEST_PARSE_ERROR_CODE_505)
# def test_parse_req_bad_http(message):
#     """If http is bad, parse request function returns error code 505."""
#     with pytest.raises(ValueError):
#         parse_request(message)
#
#
# @pytest.mark.parametrize('message', TEST_PARSE_ERROR_CODE_405)
# def test_parse_req_bad_get(message):
#     """If GET is bad, parse request function returns error code 405."""
#     with pytest.raises(ValueError):
#         parse_request(message)
