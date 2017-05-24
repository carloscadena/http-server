"""Client for http-server echo assignment."""
import socket
import sys


def client(message):
    """
    Establishe connection with the server.

    Sends message and receives reply.
    Then closes Client.
    """
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    client.connect(('127.0.0.1', 5000))
    message += '\n\r\n'
    client.sendall(message.encode('utf8'))
    buffer_length = 8
    message_complete = False
    returned = b''
    while not message_complete:
        part = client.recv(buffer_length)
        returned += part
        if b'\n\r\n' in returned:
            message_complete = True
    returned = returned[0:-3].decode('utf8')
    print(returned)
    client.close()
    return returned


if __name__ == "__main__":  # pragma: no cover
    client(sys.argv[1])
