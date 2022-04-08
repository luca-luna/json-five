from random import randint

from our_router import Route
from parsing_request import parse_form
from template import render_template
from response import file, redirect
import database

def add_paths(router):
    router.add_route(Route('GET', "/", homepage))
    router.add_route(Route('POST', "/send-chat", send_chat))


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