# -*- coding: utf-8 -*-
"""Server for http-server echo assignment."""
from __future__ import unicode_literals
import socket  # pragma: no cover
import sys  # pragma: no cover
from email.utils import formatdate


def server():  # pragma: no cover
    """
    Open the server, waits for input from client.

    Closes connection on completed message.
    Closes server with Ctrl-C
    """
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5001)
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
                if '\r\n\r\n' in message:
                    message_complete = True
            if parse_request(message) == '/index.html':
                connection.sendall(response_ok())
                connection.close()
            else:
                connection.sendall(parse_request(message))
                connection.close()
        except KeyboardInterrupt:
            print('\nServer closed good bye.')
            server.shutdown(socket.SHUT_WR)
            server.close()
            sys.exit(0)


def response_ok():
    """Send a response OK."""
    msg = b'HTTP/1.1 200 OK\r\n'
    msg += u'Date: {}\r\n\r\n'.format(formatdate(usegmt=True)).encode('utf8')
    return msg


def response_error(error_code):
    """Send a response erorr."""
    if error_code == 400:
        response = ('HTTP/1.1 ' + str(error_code) + ' Bad Request\r\n\r\n')
    elif error_code == 405:
        response = ('HTTP/1.1 ' + str(error_code) + ' Method \
Not Allowed\r\n\r\n')
    elif error_code == 505:
        response = ('HTTP/1.1 ' + str(error_code) + ' HTTP Version \
Not Supported\r\n\r\n')
    return response


def parse_request(message):
    """."""
    request_parts = message.split()
    if len(request_parts) != 5:
        return Exception(response_error(400))
    try:
        if request_parts[0] == 'GET':
        try:
            if request_parts[2] == 'HTTP/1.1':
            try:
                if request_parts[3] == 'Host:':
                    return request_parts[1].encode('utf8')
        else:
            raise
    except Exception:
        return response_error(400)
    except:
            else:
                return Exception(response_error(505))
        else:
            return Exception(response_error(405))


if __name__ == '__main__':  # pragma: no cover
    print('Server ready and waiting...')
    server()
