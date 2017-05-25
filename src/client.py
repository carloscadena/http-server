# -*- coding: utf-8 -*-
"""Client for http-server echo assignment."""
from __future__ import unicode_literals
import socket
import sys


def client(command):
    """
    Establishe connection with the server.

    Sends message and receives reply.
    Then closes Client.
    """
    try:
        client = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM,
                               socket.IPPROTO_TCP)
        client.connect(('127.0.0.1', 5001))
        command += '\r\n\r\n'
        client.sendall(command.encode('utf8'))
        buffer_length = 8
        message_complete = False
        returned = b''
        while not message_complete:
            part = client.recv(buffer_length)
            returned += part
            if b'\r\n\r\n' in returned:
                message_complete = True
        returned = returned.decode('utf8')
        returned = returned[0:-4]
        print(returned)
        client.shutdown(socket.SHUT_WR)
        client.close()
        return returned
    except KeyboardInterrupt:
        print('\nClient closed good bye.')
        client.shutdown(socket.SHUT_WR)
        client.close()
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    command = open('command.txt').read().split(' ')

    if command is not '':
        client(' '.join(command))
