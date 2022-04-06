class Request:
    new_line = b'\r\n'
    blank_line = b'\r\n\r\n'
    
    def __init__(self, request: bytes):
        #State variables/ fields to store the processed information
        [request_line, byte_headers, self.body] = split_request(request)
        [self.method, self.path, self.http_ver] = parse_request_line(request_line)
        self.headers = parse_headers(byte_headers)
        
        #self.parts = {}
        #self.tokens = []
        
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

def parse_form(bytes_request, bytes_boundary):
    boundary = b'--' + bytes_boundary
    terminating_boundary = boundary + b'--'
    form_data = {}
    request_portion = bytes_request
    end = False
    while not end:
        section_start = request_portion.find(boundary)
        request_portion = request_portion[section_start + len(boundary):]

        input_start = request_portion.find(b'\r\n\r\n')
        input_end = request_portion.find(boundary)

        headers = request_portion[:input_start].decode()
        headers = headers.split('\r\n')

        header_dict = {}

        for header in headers:
            if len(header) != 0:
                header_name_split = header.split(':')
                header_name = header_name_split[0]
                header_data = header_name_split[1].strip().split(";")
                header_dict[header_name] = {"self": header_data[0].strip()}
                for item in header_data[1:]:
                    item_data = item.strip().split('=')
                    header_dict[header_name][item_data[0]] = item_data[1].strip().strip('\"')

        input_name = header_dict['Content-Disposition']['name']
        input = request_portion[input_start + len(b'\r\n\r\n'):input_end].strip()
        header_dict['input'] = input

        form_data[input_name] = header_dict

        if input_end == request_portion.find(terminating_boundary):
            end = True

    return form_data

#Testing without having to run the server
if __name__ == "__main__":
    sample_request = ""
    request = Request(sample_request)