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



    def parse_headers(self):

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


    def extract_payload(self):
        offset = self.first_mask_or_payload_byte
        if self.maskbit == 1:
            offset = offset + 4
        raw_payload = self.frame_bytes[offset:]

        if len(raw_payload) < self.payload_length:
            return
        else:
            self.finished_buffering = True

        if self.maskbit == 1:
            mask = self.frame_bytes[self.first_mask_or_payload_byte:self.first_mask_or_payload_byte+4]
            payload = b''
            for i in range(self.first_mask_or_payload_byte+4,self.first_mask_or_payload_byte+4+self.payload_length):
                mask_byte_index = (i - self.first_mask_or_payload_byte) & 4
                payload = payload + (self.frame_bytes[i] ^ mask[mask_byte_index]).to_bytes(1, "little")
            self.payload = payload
        else:
            self.payload = self.frame_bytes[self.first_mask_or_payload_byte:self.first_mask_or_payload_byte+self.payload_length]


    def print_frame(self):

        for i in range(0, len(self.frame_bytes)):
            the_byte = self.frame_bytes[i]
            print(byte_to_binary_string(the_byte), end = " ")
            if i % 4 == 3:
                print()
            print("payload length: " + str(self.payload_length))
            print("payload: " + self.payload.decode())



def byte_to_binary_string(the_byte):

    as_binary = str(bin(the_byte))[2:]
    for i in range(len(as_binary), 8):
        as_binary = '0' + as_binary
    return as_binary


def test_frame_parsing():

    frame_bytes = b"fgjh"
    expected_message = '{}'
    frame = WSFrame(frame_bytes)
    frame.extract_payload()
    assert frame.payload_length == len(expected_message), str(frame.payload_length) + " did not equal " + str((len(expected_message)))
    assert frame.payload.decode() == expected_message, frame.payload.decode() + " did not equal " + expected_message



if __name__ == '__main__':

    test_frame_parsing()
