import hashlib
from base64 import b64encode


def compute_accept(key):
    #Sean ATTN I need to check if the concatenation of key and this string are okay, and if the .digest() is okay
    websocket_accept = key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1_websocket_accept = hashlib.sha1()
    sha1_websocket_accept.update(websocket_accept)
    base64_encoded_websocket_accept = b64encode(sha1_websocket_accept.digest())
    return base64_encoded_websocket_accept