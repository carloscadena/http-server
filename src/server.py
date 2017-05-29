# -*- coding: utf-8 -*-
"""Server for http-server echo assignment."""
from __future__ import unicode_literals
import socket  # pragma: no cover
import sys  # pragma: no cover
from email.utils import formatdate
from os import walk, path


def server():  # pragma: no cover
    """
    Open the server, waits for input from client.

    Closes connection on completed reply.
    Closes server with Ctrl-C
    """
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5006)
    server.bind(address)
    server.listen(1)
    while True:
        try:
            connection, address = server.accept()
            message = ''
            buffer_length = 8
            message_complete = False
            while not message_complete:
                part = connection.recv(buffer_length)
                message += part.decode('utf8')
                if message.endswith('\r\n\r\n'):
                    message_complete = True
            try:
                uri = parse_request(message)
                content = resolve_uri(uri)
                response = response_ok(content)
                print(response)
                connection.sendall(response.encode('utf8'))
                connection.close()
            except ValueError as error:
                connection.sendall(response_error(error.args[0]))
                connection.close()
            except IOError as error:
                connection.sendall(response_error(error.args[0]))
                connection.close()
        except KeyboardInterrupt:
            print('\nServer closed good bye.')
            server.shutdown(socket.SHUT_WR)
            server.close()
            sys.exit(0)


def response_ok(body):
    """Send a response OK, headers, and content."""
    content, content_size, content_type = body
    content_size += 9
    msg = 'HTTP/1.1 200 OK\r\n'
    msg += 'Date: {}\r\n'.format(formatdate(usegmt=True))
    msg += 'Content-Type: {}\r\n'.format(content_type)
    msg += 'Content-Length: {}\r\n\r\n'.format(content_size)
    msg += '{}'.format(content)
    return msg


def response_error(error_code):
    """Send a response erorr."""
    return ('HTTP/1.1 ' + error_code + '\r\n\r\n').encode('utf8')


def parse_request(message):
    """
    Accept request from client.

    Verify content and return appropriate error or URI.
    """
    request_parts = message.split()
    if len(request_parts) <= 5:
        raise ValueError('400 Bad Request')
    if request_parts[0] == 'GET':
        if request_parts[2] == 'HTTP/1.1':
            if request_parts[3] == 'Host:':
                return request_parts[1]
            else:
                raise ValueError('400 Bad Request')
        else:
            raise ValueError('505 HTTP Version Not Supported')
    else:
        raise ValueError('405 Method Not Allowed')


def resolve_uri(uri):
    """Take in a URI and translates it if valid or raises an error."""
    cwd = path.realpath(__file__).replace('server.py', '')
    file_path = path.join(cwd, uri[1:])
    file_type = file_path.split('.')[-1]
    content = ''
    content_size = 0
    content_type = ''
    file_type_dict = {
        'txt': 'text/plain; charset=utf-8',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'py': 'text/python',
        'html': 'text/html; charset=utf-8',
        'directory': 'directory'
    }

    for f_type in file_type_dict:
        if f_type == file_type:
            content_type = f_type
    if path.isdir(file_path):
        content_type = 'directory'
        file_dir = []
        for dirp, dirn, filen in walk(file_path):
            for file in filen:
                file_dir.append(path.join(dirp, file).replace(file_path, ''))
        html_open = '<!DOCTYPE html><html><body><h1>File Directory:</h1><ul>'
        for file in file_dir:
            html_open += '<li>{}</li>'.format(file)
        html_close = '</ul></body></html>'
        content = (html_open + html_close).encode('utf8')
        content_size = len(content)
        print(len(content))
        return content, content_size, content_type
    try:
        content_size = path.getsize(file_path)
        content = open(file_path, 'rb').read()
        print(len(content))
    except:
        raise IOError('404 File Not Found')
    return content, content_size, content_type


if __name__ == '__main__':  # pragma: no cover
    print('Server ready and waiting...')
    server()
