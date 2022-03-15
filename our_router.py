import re
from parsing_request import Request
#from util.response import generate_response

#Generating a 404-response
def four_oh_four(request, handler):
    response = "HTTP/1.1 404 Not Found\r\nContent-Length: 36\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nThe requested content does not exist".encode()
    handler.request.sendall(response)

#ROUTER
class Router:
    #Constructor
    def __init__(self):
        self.routes = []
        self.route_404 = Route('', '', four_oh_four)
    
    #Adding the route objects in our Routes list
    def add_route(self, route):
        self.routes.append(route)
    
    #Finding the correct request for our Route objects, if found perform tasks on the Route object, if not then send a 404
    def handle_request(self, request: Request, handler):
        for route in self.routes:
            if route.is_request_match(request):
                route.handle_request(request, handler)
                return
        
        self.route_404.handle_request(request, handler)
    
#ROUTE - Object for Router in the format (Method, Path, What we want to do with those two)
class Route:
    #Constructor
    def __init__(self, method, path, action):
        self.method = method
        self.path = path
        self.action = action
    
    #Comparing the received request with the stored request
    def is_request_match(self, request: Request):
        if request.method != self.method:
            return False
        search_result = re.search('^' + self.path, request.path)
        if search_result:
            return True
        else:
            return False
    
    #Calling the action fuctions
    def handle_request(self, request: Request, handler):
        self.action(request, handler)