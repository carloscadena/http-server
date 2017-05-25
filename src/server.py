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
    address = ('127.0.0.1', 5002)
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
            try:
                parse_request(message)
                connection.sendall(response_ok())
                connection.close()
            except ValueError as error:
                connection.sendall(response_error(error.args[0]))
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
    return ('HTTP/1.1 ' + error_code + '\r\n\r\n').encode('utf8')


def parse_request(message):
    """."""
    request_parts = message.split()
    if len(request_parts) != 5:
        raise ValueError('400 Bad Request')
    if request_parts[0] == 'GET':
        if request_parts[2] == 'HTTP/1.1':
            if request_parts[3] == 'Host:':
                return request_parts[1].encode('utf8')
            else:
                raise ValueError('400 Bad Request')
        else:
            raise ValueError('505 HTTP Version Not Supported')
    else:
        raise ValueError('405 Method Not Allowed')


if __name__ == '__main__':  # pragma: no cover
    print('Server ready and waiting...')
    server()
