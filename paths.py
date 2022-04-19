from random import randint
from TCPServer import MyTCPHandler

from our_router import Route
from parsing_request import parse_form
from template import render_template
from response import file, redirect, notFound, websocket_handshake, generate_response
from websocket import compute_accept
import database, random, json


def add_paths(router):
    #Adding Routes to our router
    router.add_route(Route('POST', "/send-chat", send_chat))
    router.add_route(Route('GET', "/functions.js", jsfunction))
    router.add_route(Route('GET', "/style.css", style))
    router.add_route(Route('GET', "/images/", images))
    router.add_route(Route('GET', '/websocket', websocket_request))
    router.add_route(Route('GET', '/chat-history', chat_history))
    
    #ALWAYS Keeping this at last, if you wish to add more Routes, add it above this line
    router.add_route(Route('GET', "/", homepage))


def homepage(request, handler):
    listToStr = ''.join([str(elem) for elem in request.path])
    
    if(listToStr == "/"):
        response = file("front_end/index.html")
    else:
        response = notFound()
    
    handler.request.sendall(response)
        
        

def send_chat(request, handler):
    bytes_boundary = request.headers['Content-Type'].split('=')[1].strip().encode()
    print(bytes_boundary, flush=True)
    print(request.body, flush=True)
    print(parse_form(request.body, bytes_boundary), flush=True)
    parsed_form = parse_form(request.body, bytes_boundary)
    message = escape_html(parsed_form['chat message']['input'].decode())
    username = escape_html(str(randint(0, 1000)))
    database.addHomepageMessage({"message": message, "username": username})
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

def chat_history(request, handler):
    #dummy data
    history = [{'username': 'user1', 'comment': 'hello'},
               {'username': 'user2', 'comment': 'welcome'}]
    #Sean ATTN, we just have to make this response too           
    response = generate_response(json.dumps(history).encode(), 'application/json; charset=utf-8', '200 OK')
    handler.request.sendall(response)

def websocket_request(request, handler):
    key = request.headers["Sec-WebSocket-Key"]
    accept = compute_accept(key)
    response = websocket_handshake(accept)
    handler.request.sendall(response)

    username="User"+str(random.randint(0,1000))
    MyTCPHandler.websocket_connections.append({'username':username, 'socket':handler})
    while True:
        ws_frame_raw = handler.request.recv(1024)

def escape_html(input):
    return input.replace('&', "&amp").replace('<', "&lt;").replace('>', "&gt;")
