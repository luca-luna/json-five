import hashlib
from base64 import b64encode

def compute_accept(key):
    #Sean ATTN I need to check if the concatenation of key and this string are okay, and if the .digest() is okay
    websocket_accept = key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1_websocket_accept = hashlib.sha1()
    sha1_websocket_accept.update(websocket_accept)
    base64_encoded_websocket_accept = b64encode(sha1_websocket_accept.digest())
    return base64_encoded_websocket_accept


def handshake_testing():
    key = "pBsd/kMCnKG4uza2TYIuLg=="
    expected = "5LphbGU7Oze7/0+7dcVnuPaZXzM="
    
    accept = compute_accept(key)
    assert accept == expected, accept + "is not the same as" + expected




class WSFrame:

    def __init__(self, frame_bytes):

        self.frame_bytes = frame_bytes
        self.fin = 1
        self.opcode = 0
        self.maskbit = 0

        self.payload_length = 27
        self.payload = b"12345678"
        self.first_mask_or_payload_byte = 0
        self.parse_headers()
        self.parse_payload_length()
        self.finished_buffering = False
        self.check_payload()



    def parse_header(self):

        self.opcode = self.frame_bytes[0] & 31
        self.fin = self.frame_bytes[0] >> 7
        self.maskbit = self.frame_bytes[1] >> 7


    def parse_payload_length(self):

        first_try = self.frame_bytes[1] & 127

        if first_try < 126:
            self.payload_length = first_try
            self.first_mask_or_payload_byte = 2

        elif first_try == 126:
            payload_length = int(self.frame_bytes[2])
            payload_length = payload_length << 8
            payload_length = payload_length + self.frame_bytes[3]
            self.payload_length = payload_length
            self.first_mask_or_payload_byte = 4

        elif first_try == 127:
            payload_length = int(self.frame_bytes[2])
            for i in range(3, 10):
                payload_length = payload_length << 8
                payload_length = payload_length + self.frame_bytes[i]
            self.payload_length = payload_length
            self.first_mask_or_payload_byte = 10

        else:
            print("Parsing Error: Length")



    def check_payload(self):
        return 

    
# def test_parsing_frame():
#     print()