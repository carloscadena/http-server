"""."""
import socket
import sys


def server():
    """."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
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
                if len(part) < buffer_length:
                    message_complete = True
            connection.sendall(message)
            connection.close()
        except KeyboardInterrupt:
            print('\nServer closed good bye.')
            server.close()
            sys.exit(0)


if __name__ == '__main__':
    print('Server ready and waiting...\n')
    server()
