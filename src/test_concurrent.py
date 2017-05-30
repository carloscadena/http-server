"""Test for the client server pair for echo."""
from concurrent import parse_request, resolve_uri, response_ok, response_error
from concurrent_client import client
from os import path
import pytest


html_path = path.realpath(__file__).replace('test_concurrent.py',
                                            'webroot/a_web_page.html')
jpeg_path = path.realpath(__file__).replace('test_concurrent.py',
                                            'webroot/images/JPEG_example.jpg')

png_path = path.realpath(__file__).replace('test_concurrent.py',
                                           'webroot/images/sample_1.png')
balls_path = path.realpath(__file__).replace('test_concurrent.py',
                                             'webroot/images/Sample_Scene_Balls.jpg')

with open(html_path, 'rb') as html_open:
    html_file = html_open.read()


with open(jpeg_path, 'rb') as jpeg_open:
    jpeg_file = jpeg_open.read()

with open(balls_path, 'rb') as ball_open:
    balls_file = ball_open.read()


with open(png_path, 'rb') as png_open:
    png_file = png_open.read()


dir_file = '''<!DOCTYPE html><html><body><h1>File Directory:</h1>\
<ul><li>Sample_Scene_Balls.jpg</li><li>JPEG_example.jpg</li><li>\
sample_1.png</li></ul></body></html>'''

SERVER_PARSE_OK_PARAMS = [
    ('GET /webroot/ HTTP/1.1 Host: www.yourwebsite.com:80',
        '/webroot/'),
    ('GET smelly/stuff/webroot/ HTTP/1.1 Host: www.yourwebsite.com:80',
        'smelly/stuff/webroot/'),
    ('GET bleh/bleh.html HTTP/1.1 Host: www.yourwebsite.com:80',
        'bleh/bleh.html')
]

TEST_PARSE_ERROR_CODE_400 = [
    ('GET /webroot/ HTTP/1.1 Hosts: www.yourwebsite.com:80'),
    ('GET smelly/stuff/webroot/ HTTP/1.1 Bosst: www.yourwebsite.com:80'),
    ('GET bleh/bleh.html HTTP/1.1 shmost: www.yourwebsite.com:80')
]

TEST_PARSE_ERROR_CODE_505 = [
    ('GET /webroot/ HTTPP/1.1 Hosts: www.yourwebsite.com:80'),
    ('GET smelly/stuff/webroot/ HTTP Bosst: www.yourwebsite.com:80'),
    ('GET bleh/bleh.html http/1.1 shmost: www.yourwebsite.com:80')
]

TEST_PARSE_ERROR_CODE_405 = [
    ('POST /webroot/ HTTPP/1.1 Hosts: www.yourwebsite.com:80'),
    ('get smelly/stuff/webroot/ HTTP Bosst: www.yourwebsite.com:80'),
    ('GEET bleh/bleh.html http/1.1 shmost: www.yourwebsite.com:80')
]

TEST_PARSE_ERROR_LEN_PARAMS = [
    ('GET /webroot/ HTTP/1.1 Host:'),
    ('A B C'),
    ('GET /webroot/ HTTP/1.1')
]

TEST_OK_PARAMS = [
    (b'hello world.', 12, 'string', b'HTTP/1.1 200 OK' +
        b'\r\nContent-Type: string\r\n' +
        b'Content-Length: 12\r\n\r\nhello world.\r\n\r\n'),
    (b'stuff and things.', 87, 'text', b'HTTP/1.1 200 OK' +
        b'\r\nContent-Type: text\r\n' +
        b'Content-Length: 87\r\n\r\nstuff and things.\r\n\r\n')
]

TEST_RESPONSE_ERROR_PARAMS = [
    ('400 Bad Request',
     b'HTTP/1.1 400 Bad Request\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('505 HTTP Version Not Supported',
     b'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\nSorry we could not fulfill your request.\r\n\r\n')
]

TEST_CLIENT_URI_OK_PARAMS = [
    ('GET /webroot/a_web_page.html HTTP/1.1 Host: www.google.com:80',
        'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n' +
        'Content-Length: 132\r\n\r\n' + html_file.decode('utf8') + '\r\n\r\n'),
    ('GET /webroot/images/ HTTP/1.1 Host: www.facebook.com:80',
        'HTTP/1.1 200 OK\r\nContent-Type: directory\r\n' +
        'Content-Length: 151\r\n\r\n' +
        dir_file + '\r\n\r\n'),
    ('GET /webroot/images/JPEG_example.jpg HTTP/1.1 Host: www.outlook.com:80',
        b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n' +
        b'Content-Length: 15138\r\n\r\n' +
        jpeg_file + b'\r\n\r\n')
]

TEST_CLIENT_URI_ERROR_PARAMS = [
    ('GET /webroot/images/xxx.jpg HTTP/1.1 Host: www.myspace.com:80'),
    ('GET /webroot/image HTTP/1.1 Host: www.facebooks.com:80'),
    ('GET /webroot/file_isnt_here.txt HTTP/1.1 Host: www.rotten.com:80'),
]


TEST_CLIENT_PARSE_ERROR_LEN_PARAMS = [
    ('GET /webroot/ HTTP/1.1 Host:www.google.com:80',
     'HTTP/1.1 400 Bad Request\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('GET /webroot/ HTTP/1.1Host:www.facebook.com:80',
     'HTTP/1.1 400 Bad Request\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('GETbleh/bleh.htmlHTTP/1.1Host:www.outlook.com:80',
     'HTTP/1.1 400 Bad Request\r\n\r\nSorry we could not fulfill your request.\r\n\r\n')
]


TEST_CLIENT_PARSE_ERROR_CODE_400 = [
    ('GET /webroot/ HTTP/1.1 Hosteswiththemostest: www.google.com:80',
     'HTTP/1.1 400 Bad Request\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('GET /webroot/ HTTP/1.1 Host www.facebook.com:80',
     'HTTP/1.1 400 Bad Request\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('GET bleh/bleh.html HTTP/1.1 www.outlook.com:80 Host:',
     'HTTP/1.1 400 Bad Request\r\n\r\nSorry we could not fulfill your request.\r\n\r\n')
]


TEST_CLIENT_PARSE_ERROR_CODE_405 = [
    ('GETT /webroot/ HTTP/1.1 Host: www.google.com:80',
     'HTTP/1.1 405 Method Not Allowed\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('PUT /webroot/ HTTP/1.1 Host: www.facebook.com:80',
     'HTTP/1.1 405 Method Not Allowed\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('Wookie bleh/bleh.html HTTP/1.1 Host: www.outlook.com:80',
     'HTTP/1.1 405 Method Not Allowed\r\n\r\nSorry we could not fulfill your request.\r\n\r\n')
]


TEST_CLIENT_PARSE_ERROR_CODE_505 = [
    ('GET /webroot/ HTP/11 Host: www.google.com:80',
     'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('GET /webroot/ HTTPS/1.1 Host: www.facebook.com:80',
     'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\nSorry we could not fulfill your request.\r\n\r\n'),
    ('GET bleh/bleh.html HTTP/2.1 Host: www.outlook.com:80',
     'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\nSorry we could not fulfill your request.\r\n\r\n')
]


TEST_RESOLVE_URI_JPG_PARAMS = [
    ('/webroot/images/JPEG_example.jpg', jpeg_file, 15138, 'image/jpeg'),
    ('/webroot/images/Sample_Scene_Balls.jpg', balls_file, 146534, 'image/jpeg')
]

TEST_RESOLVE_URI_PNG = [
    ('/webroot/images/sample_1.png',
     png_file, 8760, 'image/png')
]

TEST_RESOLVE_URI_TXT = [
    ('/webroot/sample.txt',
     b'''This is a very simple text file.
Just to show that we can serve it up.
It is three lines long.
''',
     95, 'text/plain; charset=utf-8'),
]

TEST_RESOLVE_URI_HTML = [
    ('/webroot/a_web_page.html',
     b'''<!DOCTYPE html>\n<html>\n  <body>
    <h1>Code Fellows</h1>
    <p>A fine place to learn Python web programming!</p>
  </body>\n</html>''',
     132,
     'text/html; charset=utf-8')
]


TEST_RESOLVE_URI_PY = [
    ('/webroot/make_time.py',
     b'''#!/usr/bin/env python\n
"""\nmake_time.py\n
simple script that returns and HTML page with the current time\n"""\n
import datetime\n\ntime_str = datetime.datetime.now().isoformat()\n
html = """\n<http>\n<body>\n<h2> The time is: </h2>\n<p> %s <p>\n</body>\n</http>
""" % time_str\n\nprint(html)\n''',
     278, 'text/python')

]


TEST_RESOLVE_URI_DIR = [
    ('/webroot/',
     b'<!DOCTYPE html><html><body><h1>File Directory:</h1><ul><li>a_web_page.html</li><li>make_time.py</li><li>sample.txt</li><li>images/Sample_Scene_Balls.jpg</li><li>images/JPEG_example.jpg</li><li>images/sample_1.png</li></ul></body></html>',
     236, 'directory')

]

TEST_RESOLVE_URI_ERROR_PARAMS = [
    ('/A/BAD/DIRECTORY'),
    ('/webroot/videos'),
    ('/webroot/images/xxx.jpg')
]


@pytest.mark.parametrize('message, result', SERVER_PARSE_OK_PARAMS)
def test_server_parse_request_ok(message, result):
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
    """Test return of error message from response error function."""
    assert response_error(code) == result


@pytest.mark.parametrize('content, content_size, content_type, result', TEST_OK_PARAMS)
def test_response_ok(content, content_size, content_type, result):
    """Test message send and recieve."""
    body = content, content_size, content_type
    assert response_ok(body) == result


@pytest.mark.parametrize('message, result', TEST_CLIENT_URI_OK_PARAMS)
def test_client_resolve_uri_ok(message, result):
    """Test resolve URI function returns properly formatted response."""
    assert client(message) == result


@pytest.mark.parametrize('message', TEST_CLIENT_URI_ERROR_PARAMS)
def test_client_resolve_uri_error(message):
    """."""
    with pytest.raises(IOError):
        resolve_uri(message)


@pytest.mark.parametrize('message, result', TEST_CLIENT_PARSE_ERROR_LEN_PARAMS)
def test_client_parse_req_bad_len(message, result):
    """Test the length function in the parse request function."""
    assert client(message) == result


@pytest.mark.parametrize('message, result', TEST_CLIENT_PARSE_ERROR_CODE_400)
def test_client_parse_req_bad_host(message, result):
    """If host is bad, parse request function returns error code 400."""
    assert client(message) == result


@pytest.mark.parametrize('message, result', TEST_CLIENT_PARSE_ERROR_CODE_405)
def test_client_parse_req_bad_http(message, result):
    """If http is bad, parse request function returns error code 505."""
    assert client(message) == result


@pytest.mark.parametrize('message, result', TEST_CLIENT_PARSE_ERROR_CODE_505)
def test_client_parse_req_bad_get(message, result):
    """If GET is bad, parse request function returns error code 405."""
    assert client(message) == result


@pytest.mark.parametrize('uri, body, content_length, file_type', TEST_RESOLVE_URI_JPG_PARAMS)
def test_resolve_uri_jpg(uri, body, content_length, file_type):
    """."""
    assert resolve_uri(uri) == (body, content_length, file_type)


@pytest.mark.parametrize('uri, body, content_length, file_type', TEST_RESOLVE_URI_PNG)
def test_resolve_uri_png(uri, body, content_length, file_type):
    """."""
    assert resolve_uri(uri) == (body, content_length, file_type)


@pytest.mark.parametrize('uri, body, content_length, file_type', TEST_RESOLVE_URI_TXT)
def test_resolve_uri_txt(uri, body, content_length, file_type):
    """."""
    assert resolve_uri(uri) == (body, content_length, file_type)


@pytest.mark.parametrize('uri, body, content_length, file_type', TEST_RESOLVE_URI_HTML)
def test_resolve_uri_html(uri, body, content_length, file_type):
    """."""
    assert resolve_uri(uri) == (body, content_length, file_type)


@pytest.mark.parametrize('uri, body, content_length, file_type', TEST_RESOLVE_URI_PY)
def test_resolve_uri_py(uri, body, content_length, file_type):
    """."""
    assert resolve_uri(uri) == (body, content_length, file_type)


@pytest.mark.parametrize('uri, body, content_length, file_type', TEST_RESOLVE_URI_DIR)
def test_resolve_uri_dir(uri, body, content_length, file_type):
    """."""
    assert resolve_uri(uri) == (body, content_length, file_type)


@pytest.mark.parametrize('uri', TEST_RESOLVE_URI_ERROR_PARAMS)
def test_resolve_uri_error(uri):
    """."""
    with pytest.raises(IOError):
        resolve_uri(uri)


# def test_close_down_files():
#     """."""
#     jpeg_file.close(jpeg_path, 'rb')
#     png_file.close(png_path, 'rb')
