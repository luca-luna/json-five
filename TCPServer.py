import socketserver
import sys
import response
import database
from parsing_request import Request
from our_router import Router
import paths as path

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    counter = 0
    #Storing the websocket connections 
    websocket_connections = []
    #Storing the usernames for the connections
    #user_dictionary = {}
     #CONSTRUCTOR
    def __init__(self, request, client_addr, server):
       self.router = Router()
       path.add_paths(self.router)
       super().__init__(request, client_addr, server)
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024)
        #.strip()
        request = Request(data)
        #BUFFERING
        print("Before Buffering")
        if "Content-Length" in request.headers.keys():
            while (len(request.body) < int(request.headers["Content-Length"])):
                data += self.request.recv(1024)
                request = Request(data)
            self.data = data
        
        print("--------------------------------------------------------------------------------------------------------------------------")
        print(data)
        print("--------------------------------------------end of data---------------------------------------------------------------\n\n")
        print(request.headers)
        print("--------------------------------------------end of headers---------------------------------------------------------------\n\n")
        
        sys.stdout.flush()
        sys.stderr.flush()
        
        self.router.handle_request(request, self)


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

    '''
    DB TESTS
    homepage_message_info = {"message": "hi friends", "username": "Rob"}
    print("create homepage message", database.addHomepageMessage(homepage_message_info), flush=True)
    homepage_message_info2 = {"message": "hello", "username": "Sam"}
    print("create homepage message 2", database.addHomepageMessage(homepage_message_info2), flush=True)
    homepage_messages = database.listHomepageMessages()
    print("homepage messages", homepage_messages, flush=True)
    dm_info = {"message": "hi dude", "username1": "Debbie", "username2": "Rob"}
    print("create dm", database.addDM(dm_info), flush=True)
    dm_info2 = {"message": "yo", "username1": "Rob", "username2": "Debbie"}
    print("create dm2", database.addDM(dm_info2), flush=True)
    dm_info3 = {"message": "what is your favorite color?", "username1": "Sam", "username2": "Emily"}
    print("create dm3", database.addDM(dm_info3), flush=True)
    dm_info4 = {"message": "red", "username1": "Emily", "username2": "Sam"}
    print("create dm4", database.addDM(dm_info4), flush=True)
    dm_info5 = {"message": "cool, mine is blue", "username1": "Sam", "username2": "Emily"}
    print("create dm5", database.addDM(dm_info5), flush=True)
    dm_messages = database.listDMs("Debbie", "Rob")
    print("dm messages", dm_messages, flush=True)
    dm_messages2 = database.listDMs("Emily", "Sam")
    print("dm messages2", dm_messages2, flush=True)
    '''

    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()