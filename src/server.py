"""."""
import socket
import sys


def server():
    """."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5000)
        server.bind(address)
        server.listen(1)
        connection, address = server.accept()
        message = ''
        buffer_length = 8
        message_complete = False
        while not message_complete:
            part = connection.recv(buffer_length)
            message += (part.decode('utf8'))
            if len(part) < buffer_length:
                message_complete = True
        connection.sendall(message.encode('utf8'))
        connection.close()
    except KeyboardInterrupt:
        print('\nInterupted')
        sys.exit(0)
