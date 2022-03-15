import re
from parsing_request import Request
#from util.response import generate_response
#from util.response import four_oh_four

class Router:
    def __init__(self):
        self.routes = []
        self.route_404 = Route('', '', four_oh_four)
        
    def add_route(self, route):
        self.routes.append(route)
    
    def handle_request(self, request: Request, handler):
        for route in self.routes:
            if route.is_request_match(request):
                route.handle_request(request, handler)
                return
        
        self.route_404.handle_request(request, handler)
        

class Route:
    def __init__(self, method, path, action):
        self.method = method
        self.path = path
        self.action = action
    
    def is_request_match(self, request: Request):
        if request.method != self.method:
            return False
        search_result = re.search('^' + self.path, request.path)
        if search_result:
            return True
        else:
            return False
    
    def handle_request(self, request: Request, handler):
        self.action(request, handler)