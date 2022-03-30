import socketserver
import response
import database

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