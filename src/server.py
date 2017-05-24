"""Server for http-server echo assignment."""
import socket  # pragma: no cover
import sys  # pragma: no cover
import email.utils


date = email.utils.formatdate(usegmt=True)


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
            connection.sendall(response_ok())
            connection.close()
        except KeyboardInterrupt:
            print('\nServer closed good bye.')
            server.close()
            sys.exit(0)


def response_ok():
    """Send a response OK."""
    return b'HTTP/1.1 200 OK\r\nMessage recieved.\n\r\n'


def response_error():
    """Send a response erorr."""
    return b'HTTP/1.1 500 Internal Server Error\r\nError!'


if __name__ == '__main__':  # pragma: no cover
    print('Server ready and waiting...\n')
    server()
