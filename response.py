import parse

def file(filename):

    file = open(filename, 'rb')

    content = bytes()
    for line in file:
        content += line

    file.close()

    file_type = parse.fileType(filename)

    if file_type == "jpg":
        content_type = "image/jpeg"
    else:
        content_type = "text/" + file_type + "; charset=utf-8"

    print("content type", content_type, flush=True)

    response = ok(content_type, content)

    return response


def forbidden():
    return "HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 50\r\n\r\nYou do not have permission to access this resource".encode()


def ok(content_type, message):

    header = ("HTTP/1.1 200 OK\r\nContent-Length: " + str(len(message)) + "\r\nContent-Type: " + content_type + "\r\nX-Content-Type-Options: nosniff\r\n\r\n").encode()
    print("header", header, flush=True)
    response = header + message
    print("response", response, flush=True)
    return response


def redirect(new_location):
    return ("HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: " + new_location + "\r\n\r\n").encode()


def notFound():
     return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 36\r\n\r\nThe requested content does not exist".encode()


