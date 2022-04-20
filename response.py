import parse
from database import message_collection, listHomepageMessages, listImages
from database import username_posted_collection
from template import render_template

def generate_response(body: bytes, content_type: str = 'text/plain; charset=utf-8', response_code: str = '200 OK'):
    response = b'HTTP/1.1 ' + response_code.encode()
    response += b'\r\nContent-Length: ' + str(len(body)).encode()
    response += b'\r\nContent-Type: ' + content_type.encode()
    response += b'\r\nX-Content-Type-Options: nosniff'
    response += b'\r\n\r\n'
    response += body
  
    return response

def file(filename):

    file = open(filename, 'rb')

    content = bytes()
    for line in file:
        content += line

    file.close()

    file_type = parse.fileType(filename)

    if file_type == "jpg":
        content_type = "image/jpeg"

    elif file_type == "html":
        print(listHomepageMessages(), flush=True)
        content = render_template(filename, {"loop_data2": listHomepageMessages(), "loop_data3": listImages()}).encode()
        print(content, flush=True)
        content_type = "text/html; charset=utf-8"

        # messages = list(message_collection.find({}, {'_id': False}))
        # usernames = list(username_posted_collection.find({}, {"_id": False}))
        #
        # replace = ""
        # for i in range(len(messages)):
        #     replace += "<p>"
        #     replace += usernames[i]["username"] + ">> "
        #     replace += messages[i]["message"]
        #     replace += "</p>"
        #
        # content = content.replace(b"{{loop2}}", b"")
        # content = content.replace(b"{{end_loop2}}", b"")
        # content = content.replace(b"{{username}}: {{message}}", replace.encode())
        # content_type = "text/" + file_type + "; charset=utf-8"

    else:
        content_type = "text/" + file_type + "; charset=utf-8"

    print("content type", content_type, flush=True)

    response = ok(content_type, content)
    # print(respost, flush=True)

    return response


def forbidden():
    return "HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 50\r\n\r\nYou do not have permission to access this resource".encode()


def ok(content_type, message):

    header = ("HTTP/1.1 200 OK\r\nContent-Length: " + str(len(message)) + "\r\nContent-Type: " + content_type + "\r\nX-Content-Type-Options: nosniff\r\n\r\n").encode()
    print("header", header, flush=True)
    response = header + message
    print("response", response, flush=True)
    return response

def websocket_handshake(accept):

    #Sean ATTN, kept it like this for now
    response = ("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: " + accept + "\r\n\r\n").encode()
    return response


def redirect(new_location):
    return ("HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: " + new_location + "\r\n\r\n").encode()


def notFound():
     return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 36\r\n\r\nThe requested content does not exist".encode()
