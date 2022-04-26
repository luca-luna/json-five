from random import randint
from TCPServer import MyTCPHandler

from our_router import Route
from parsing_request import parse_form
from template import render_template
from response import file, redirect, notFound, websocket_handshake, generate_response
from websocket import compute_accept
import database, random, json
import websocket

from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client['312-Project']
user_collection = db['users']
message_collection = db['messages']
dm_collection = db['dms']

def add_paths(router):
    #Adding Routes to our router
    router.add_route(Route('POST', "/send-chat", send_chat))
    router.add_route(Route('GET', "/functions.js", jsfunction))
    router.add_route(Route('GET', "/style.css", style))
    router.add_route(Route('GET', "/images/", images))
    router.add_route(Route('GET', '/websocket', websocket_request))
    router.add_route(Route('GET', '/chat-history', chat_history))
    router.add_route(Route('GET', "/connect_websocket.js", wsfunction))
    
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
    # print(bytes_boundary, flush=True)
    # print(request.body, flush=True)
    # print(parse_form(request.body, bytes_boundary), flush=True)
    parsed_form = parse_form(request.body, bytes_boundary)
    message = escape_html(parsed_form['chat message']['input'].decode())
    username = escape_html(str(randint(0, 1000)))
    database.addHomepageMessage({"message": message, "username": username, "upvotes": 0})
    # print("inserted", flush=True)
    handler.request.sendall(redirect("/"))

def jsfunction(request, handler):
    response = file("front_end/functions.js")
    handler.request.sendall(response)

def wsfunction(request, handler):
    response = file("front_end/connect_websocket.js")
    handler.request.sendall(response)
    
def style(request, handler):
    response = file("front_end/style.css")
    handler.request.sendall(response)
    
def images(request, handler):
    path_prefix = "/images/"
    image_name = request.path[request.path.find(path_prefix) + len(path_prefix):]
    # print("Our image")
    # print(image_name)
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
    print("key", key, flush=True)
    accept = compute_accept(key)
    print("accept", flush=True)
    response = websocket_handshake(accept)
    print("websocket", response, flush=True)
    handler.request.sendall(response)

    username="User"+str(random.randint(0,1000))
    MyTCPHandler.websocket_connections.append({'username':username, 'socket':handler})
    while True:
        ws_frame_raw = handler.request.recv(1024)
        ws_frame = websocket.WSFrame(ws_frame_raw)
        if ws_frame.opcode == 8:
            print("disconnecting")
            print(MyTCPHandler.websocket_connections)
            to_delete = None
            for connection in MyTCPHandler.websocket_connections:
                if connection['socket'] == handler:
                    to_delete = connection
            if to_delete:
                MyTCPHandler.websocket_connections.remove(to_delete)
            print(MyTCPHandler.websocket_connections)
            break

        while not ws_frame.finished_buffering:
            ws_frame_raw += handler.request.recv(1024)
            ws_frame.check_payload()
        ws_frame.extract_payload()
        message_json = ws_frame.payload.decode()
        message = json.loads(message_json)
        message_type = message['messageType']
        response = websocket_handle(message)
        if message_type == "upvoteMessage":
            for connection in MyTCPHandler.websocket_connections:
                connection['socket'].request.sendall(response)
        if message_type == "directMessage":
            for connection in MyTCPHandler.websocket_connections:
                connection['socket'].request.sendall(response)

def websocket_handle(message):
    print("handle", message, flush=True)
    if message['messageType'] == 'upvoteMessage':
        # Update database
        upvotes = message_collection.find_one({'id': message['message_id']})['upvotes'] + 1
        message_collection.update_one({'id': message['message_id']}, {'$set': {'upvotes': upvotes}})
        # Make response with new count
        return websocket.generate_frame(json.dumps({'messageType': 'upvoteMessage', 'id': str(message['message_id']), 'upvoteCount': str(upvotes)}).encode())
    if message['messageType'] == 'directMessage':
        # Update database
        dm_collection.insert_one({'messageType': 'directMessage'}, {'$set': {'message': message['message']}})
        # Make response with new count
        return websocket.generate_frame(json.dumps({'messageType': 'directMessage', 'message': message['message']}).encode())

def escape_html(input):
    return input.replace('&', "&amp").replace('<', "&lt;").replace('>', "&gt;")
