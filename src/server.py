"""Server for http-server step3 assignment."""
import socket  # pragma: no cover
import sys  # pragma: no cover
from os import walk, path


def server():  # pragma: no cover
    """
    Open the server, waits for input from client.

    Closes connection on completed reply.
    Closes server with Ctrl-C
    """
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5001)
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
                if message.endswith('\r\n\r\n'):
                    message_complete = True
            try:
                uri = parse_request(message)
                content = resolve_uri(uri)
                response = response_ok(content)
                connection.sendall(response)
                connection.close()
            except ValueError as error:
                response = response_error(error.args[0])
                connection.sendall(response)
                connection.close()
            except IOError as error:
                response = response_error(error.args[0])
                connection.sendall(response)
                connection.close()
        except KeyboardInterrupt:
            print('\nServer closed good bye.')
            server.shutdown(socket.SHUT_WR)
            server.close()
            sys.exit(0)


def response_ok(body):
    """Send a response OK, headers, and content."""
    content, content_size, content_type = body
    msg = b'HTTP/1.1 200 OK\r\nContent-Type: '
    msg += content_type.encode('utf8')
    msg += b'\r\nContent-Length: '
    msg += str(content_size).encode('utf8')
    msg += b'\r\n\r\n'
    msg += content
    msg += b'\r\n\r\n'
    return msg


def response_error(error_code):
    """Send a response erorr."""
    err = ('HTTP/1.1 ' + error_code + '\r\n\r\n').encode('utf8')
    err += b'Sorry we could not fulfill your request.\r\n\r\n'
    return err


def parse_request(message):
    """
    Accept request from client.

    Verify content and return appropriate error or URI.
    """
    request_parts = message.split()
    if len(request_parts) <= 4:
        raise ValueError('400 Bad Request')
    if request_parts[0] == 'GET':
        if request_parts[2] == 'HTTP/1.1':
            if request_parts[3] == 'Host:':
                return request_parts[1]
            else:
                raise ValueError('400 Bad Request')
        else:
            raise ValueError('505 HTTP Version Not Supported')
    else:
        raise ValueError('405 Method Not Allowed')


def resolve_uri(uri):
    """Take in a URI and translates it if valid or raises an error."""
    cwd = path.realpath(__file__).replace('server.py', 'webroot/')
    file_path = path.join(cwd, uri[1:])
    file_type = file_path.split('.')[-1]
    content = ''
    content_size = 0
    content_type = ''
    file_type_dict = {
        'txt': 'text/plain; charset=utf-8',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'py': 'text/python',
        'html': 'text/html; charset=utf-8',
    }

    for f_type in file_type_dict:
        if f_type == file_type:
            content_type = file_type_dict[f_type]
    file_dir = []
    for dpath, dname, fname in walk(file_path):
        for file in fname:
            file_dir.append(path.join(dpath, file).replace(file_path, ''))
    if path.isdir(file_path):
        content_type = 'directory'
        html_open = '<!DOCTYPE html><html><body><h1>File Directory:</h1><ul>'
        for file in file_dir:
            html_open += '<li>{}</li>'.format(file)
        html_close = '</ul></body></html>'
        content = (html_open + html_close).encode('utf8')
        content_size = len(content)
        return content, content_size, content_type
    elif path.isfile(file_path):
        content_size = path.getsize(file_path)
        with open(file_path, 'rb') as content:
            content = content.read()
        return content, content_size, content_type
    else:
        raise IOError('404 File Not Found')


if __name__ == '__main__':  # pragma: no cover
    print('Server ready and waiting...')
    server()
