import socketserver
import response

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("test", flush=True)
        print("{} wrote:".format(self.client_address[0]), flush=True)
        print(self.data, flush=True)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000

    '''
    RESPONSE TESTS
    print("not found", response.notFound(),flush=True)
    print("redirect", response.redirect("/yo"), flush=True)
    print("forbidden", response.forbidden(), flush=True)
    print("ok", response.ok("text/plain; charset=utf-8", "LOL".encode()), flush=True)
    print("file", response.file("front_end/index.html"), flush=True)
    '''

    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()