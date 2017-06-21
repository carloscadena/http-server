"""Client for http-server step3 assignment."""
import socket
import sys


def client(command):
    """
    Establishe connection with the server.

    Sends message and receives reply.
    Then closes Client.
    Optional close with ctrl-c if client/server hang.
    """
    try:
        client = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM,
                               socket.IPPROTO_TCP)
        client.connect(('127.0.0.1', 5002))
        command += '\r\n\r\n'
        client.sendall(command.encode('utf8'))
        buffer_length = 32
        message_complete = False
        returned = b''
        while not message_complete:
            part = client.recv(buffer_length)
            returned += part
            if returned.endswith(b'\r\n\r\n'):
                message_complete = True
        returned = returned.decode('utf8')
        client.shutdown(socket.SHUT_WR)
        client.close()
        return returned
    except UnicodeDecodeError:
        client.shutdown(socket.SHUT_WR)
        client.close()
        return returned
    except KeyboardInterrupt:  # pragma: no cover
        print('\nClient closed good bye.')
        client.shutdown(socket.SHUT_WR)
        client.close()
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    command = open('command.txt').read().split(' ')

    if command is not '':
        client(' '.join(command))
