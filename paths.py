from random import randint

from our_router import Route
from parsing_request import parse_form
from template import render_template
from response import file, redirect
import database

def add_paths(router):
    #Adding Routes to our router
    router.add_route(Route('POST', "/send-chat", send_chat))
    router.add_route(Route('GET', "/functions.js", jsfunction))
    router.add_route(Route('GET', "/style.css", style))
    router.add_route(Route('GET', "/images/", images))
    
    #ALWAYS Keeping this at last, if you wish to add more Routes, add it above this line
    router.add_route(Route('GET', "/", homepage))


def homepage(request, handler):
    listToStr = ''.join([str(elem) for elem in request.path])
    
    if(listToStr == "/"):
        response = file("front_end/index.html")
        handler.request.sendall(response)

def send_chat(request, handler):
    bytes_boundary = request.headers['Content-Type'].split('=')[1].strip().encode()
    print(bytes_boundary, flush=True)
    print(request.body, flush=True)
    print(parse_form(request.body, bytes_boundary), flush=True)
    parsed_form = parse_form(request.body, bytes_boundary)
    database.addHomepageMessage({"message": parsed_form['chat message']['input'].decode(), "username": str(randint(0, 1000))})
    print("inserted", flush=True)
    handler.request.sendall(redirect("/"))

def jsfunction(request, handler):
    response = file("front_end/functions.js")
    handler.request.sendall(response)
    
def style(request, handler):
    response = file("front_end/style.css")
    handler.request.sendall(response)
    
def images(request, handler):
    path_prefix = "/images/"
    image_name = request.path[request.path.find(path_prefix) + len(path_prefix):]
    print("Our image")
    print(image_name)
    image_name = image_name.replace("/", "")
    response = file("front_end/images/" + image_name)
    handler.request.sendall(response)