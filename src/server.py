# -*- coding: utf-8 -*-
"""Server for http-server echo assignment."""
from __future__ import unicode_literals
import socket  # pragma: no cover
import sys  # pragma: no cover


def server():  # pragma: no cover
    """
    Open the server, waits for input from client.

    Closes connection on completed message.
    Closes server with Ctrl-C
    """
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    while True:
        try:
            connection, address = server.accept()

            message = b''
            buffer_length = 8
            message_complete = False
            while not message_complete:
                part = connection.recv(buffer_length)
                message += part
                if b'\n\r\n' in message:
                    message_complete = True
            connection.sendall(message)
            connection.close()
        except KeyboardInterrupt:
            print('\nServer closed good bye.')
            server.close()
            sys.exit(0)


if __name__ == '__main__':  # pragma: no cover
    print('Server ready and waiting...')
    server()
