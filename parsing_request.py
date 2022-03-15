class Request:
    new_line = b'\r\n'
    blank_line = b'\r\n\r\n'
    
    def __init__(self, request: bytes):
        #State variables/ fields to store the processed information
        [request_line, byte_headers, self.body] = split_request(request)
        [self.method, self.path, self.http_ver] = parse_request_line(request_line)
        self.headers = parse_headers(byte_headers)
        
def split_request(request: bytes):
    #Looking for the 1st new line character and split on that
    first_newline = request.find(Request.new_line)
    #Looking for the 1st blank line character and split on that
    blank_line_boundary = request.find(Request.blank_line)
    
    #Before the 1st new line -> Request line
    request_line = request[:first_newline]
    #After the 1st new line & before the 1st blank line -> Headers
    byte_headers = request[(first_newline + len(Request.new_line)):blank_line_boundary]
    #Efter the 1st blank line -> Body
    body = request[(blank_line_boundary + len(Request.blank_line)):]
    
    return [request_line, byte_headers, body]

def parse_request_line(request_line: bytes):
    return request_line.decode().split(' ')

def parse_headers(headers: bytes):
    #Dictionary of headers - Header : Value
    myHeaders = {}
    #Headers have strict format so it's safe to use split on the new line now
    lines_as_str = headers.decode().split(Request.new_line.decode())
    #For each header
    for line in lines_as_str:
        #Separate the value & getting rid of the extra white space after the ':'
        splits = line.split(':')
        myHeaders[splits[0].strip()] = splits[1].strip()
    return myHeaders

#Testing without having to run the server
if __name__ == "__main__":
    sample_request = ""
    request = Request(sample_request)