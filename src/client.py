import socket


def client(message):
    addr_info = socket.getaddrinfo('127.0.0.1', 8989)
    stream_info = [attr for attr in addr_info if attr[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    buffer_length = 8
    message_complete = False
    returned = ''
    while not message_complete:
        part = client.recv(buffer_length)
        returned += part
        if len(part) < buffer_length:
            print(returned.decode('utf8'))
            connection.close()
            client.close()
            message_complete = True

    connection.sendall(message.encode('utf8'))


if __name__ == "__main__":
    client()
