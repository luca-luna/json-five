from our_router import Route
from template import render_template
from response import file
import database

def add_paths(router):
    router.add_route(Route('GET', "/", homepage))


def homepage(request, handler):
    listToStr = ''.join([str(elem) for elem in request.path])
    
    if(listToStr == "/"):
        response = file("./index.html")
        handler.request.sendall(response)