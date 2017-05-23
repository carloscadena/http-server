"""."""
import socket
import sys


def client(message):
    """."""
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    client.connect(('127.0.0.1', 5000))
    client.sendall(message.encode('utf8'))
    buffer_length = 8
    message_complete = False
    returned = ''
    while not message_complete:
        part = client.recv(buffer_length)
        returned += part.decode('utf8')
        if len(part) < buffer_length:
            print(returned)
            message_complete = True
    client.close()


if __name__ == "__main__":
    client(sys.argv[1])
