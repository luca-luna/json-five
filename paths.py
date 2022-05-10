import base64
import hashlib
import uuid
from random import randint

import bcrypt as bcrypt

from TCPServer import MyTCPHandler

from our_router import Route
from parsing_request import parse_form, split_request, parse_request_line, parse_headers
from template import render_template
from response import file, redirect, notFound, websocket_handshake, generate_response, forbidden, response_301
from websocket import compute_accept
import database, random, json
import websocket
import parse
from database import image_collection, image_id_collection

from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client['312-Project']
user_collection = db['users']
message_collection = db['messages']
dm_collection = db['dms']
account_collection = db["accounts"]

def add_paths(router):
    #Adding Routes to our router
    router.add_route(Route('POST', "/send-chat", send_chat))
    router.add_route(Route('POST', "/image-upload", image_upload))
    router.add_route(Route('GET', "/functions.js", jsfunction))
    router.add_route(Route('GET', "/style.css", style))
    router.add_route(Route('GET', "/images/", images))
    router.add_route(Route('GET', '/websocket', websocket_request))
    router.add_route(Route('GET', '/chat-history', chat_history))
    router.add_route(Route('GET', "/connect_websocket.js", wsfunction))
    router.add_route(Route('POST', "/signup", signup))
    router.add_route(Route('POST', "/login", login))
    
    #ALWAYS Keeping this at last, if you wish to add more Routes, add it above this line
    router.add_route(Route('GET', "/", homepage))


def homepage(request, handler):
    listToStr = ''.join([str(elem) for elem in request.path])
    
    if(listToStr == "/"):
        response = file("front_end/index.html", get_username(request))
    else:
        response = notFound()
    
    handler.request.sendall(response)


def get_username(request):
    headers = request.headers
    if 'Cookie' not in headers.keys():
        return ""
    cookies = headers['Cookie'].split(';')
    auth_cookie = ""
    for cookie in cookies:
        parsed_cookie = cookie.split('=')
        if parsed_cookie[0].strip() == "id":
            auth_cookie = parsed_cookie[1].strip()
            print("id:", auth_cookie, flush=True)
            break
    if auth_cookie != "" and auth_cookie != "-1":
        account_data = account_collection.find()
        hashed_cookie = hashlib.sha256(auth_cookie.encode()).digest()
        for entry in account_data:
            print(entry["cookie"], auth_cookie)
            if entry["cookie"] == hashed_cookie:
                print("account found", flush=True)
                return entry["username"].decode()
    return ""
        
def image_upload(request, handler):
    # get image bytes
    bytes_boundary = request.headers['Content-Type'].split('=')[1].strip().encode()
    parsed_form = parse_form(request.body, bytes_boundary)
    image_bytes = parsed_form['upload']['input']

    # add image path to database
    username = get_username(request)
    print("username", username, flush=True)
    xsrf_token = parsed_form['xsrf_token']['input'].decode()
    print("xsrf token", xsrf_token, flush=True)

    if username != "" and parse.verifyXSRFToken(xsrf_token, account_collection):
        print("adding message to DB", flush=True)
        image_path = database.addImage(username)
        print("IMAGE PATH")
        print(image_path, flush=True)

        # write bytes to a file at filepath
        with open('front_end/' + str(image_path), 'wb') as f:
            f.write(image_bytes)
            print("FILE WRITTEN")

    handler.request.sendall(redirect("/"))


def send_chat(request, handler):
    bytes_boundary = request.headers['Content-Type'].split('=')[1].strip().encode()
    # print(bytes_boundary, flush=True)
    # print(request.body, flush=True)
    # print(parse_form(request.body, bytes_boundary), flush=True)
    print("about to parse form", flush=True)
    parsed_form = parse_form(request.body, bytes_boundary)
    print("parsed form", parsed_form, flush=True)
    message = escape_html(parsed_form['chat message']['input'].decode())
    print("about to get username", flush=True)
    username = get_username(request)
    print("username", username, flush=True)
    xsrf_token = parsed_form['xsrf_token']['input'].decode()
    print("xsrf token", xsrf_token, flush=True)

    if username != "" and parse.verifyXSRFToken(xsrf_token, account_collection):
        print("adding message to DB", flush=True)
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
    if "/" in image_name:
        response = forbidden()
    else:
        image_name = image_name.replace("/", "")
        response = file("front_end/images/" + image_name)
        print("serving: " + "front_end/images/" + image_name)
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

    username = ""
    if 'Cookie' in request.headers.keys():
        cookies = request.headers['Cookie'].split(';')
        print("Cookies:", cookies, flush=True)
        for cookie in cookies:
            parsed_cookie = cookie.split('=')
            print(parsed_cookie, flush=True)
            if parsed_cookie[0].strip() == "id":
                auth_cookie = parsed_cookie[1].strip()
                print(auth_cookie, flush=True)
                hashed_cookie = hashlib.sha256(auth_cookie.encode()).digest()
                print(hashed_cookie, flush=True)
                username = account_collection.find_one({'cookie': hashed_cookie})
                print(username, flush=True)
                username = username["username"]

    print(username, flush=True)
    MyTCPHandler.websocket_connections.append({'username':username, 'socket':handler})
    print(MyTCPHandler.websocket_connections, flush=True)

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
        message['sender'] = username.decode()
        response = websocket_handle(message)
        if message_type == "upvoteMessage":
            for connection in MyTCPHandler.websocket_connections:
                connection['socket'].request.sendall(response)
        if message_type == "directMessage":
            recipient = message['recipient']
            for connection in MyTCPHandler.websocket_connections:
                if(connection['username'].decode() == recipient):
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
        dm_collection.insert_one({'messageType': 'directMessage', 'recipient': message['recipient'], 'sender': message['sender']}, {'$set': {'message': message['message']}})
        # Make response with new count
        print(message['sender'])
        return websocket.generate_frame(json.dumps({'messageType': 'directMessage', 'message': message['message'], 'recipient': message['recipient'], 'sender': message['sender']}).encode())

def escape_html(input):
    return input.replace('&', "&amp").replace('<', "&lt;").replace('>', "&gt;")

def signup(request, handler):
    # Get parser info
    body = request.body
    headers = request.headers

    # Find boundary
    boundary = headers["Content-Type"].split('=')[1].strip()

    form_data = parse_form(body.strip(), boundary.encode())
    print(form_data, flush=True)

    username = form_data['signup-username']['input']
    username = escape_html(username.decode()).encode()
    password = form_data['signup-password']['input']
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password).digest()), salt)

    # Check if username already exists
    account_data = account_collection.find()
    for entry in account_data:
        if entry["username"] == username:
            print("duplicate username", flush=True)
            handler.request.sendall(response_301("/"))

    print(username, password)
    account_collection.insert_one(
        {"username": username, "password": password, "cookie": "-1", "salt": salt, "xsrf_token": "-1"})
    print("account created")
    handler.request.sendall(response_301("/"))

def login(request, handler):
    # Get parser info
    body = request.body
    headers = request.headers

    # Find boundary
    boundary = headers["Content-Type"].split('=')[1].strip()

    form_data = parse_form(body.strip(), boundary.encode())

    username = form_data['login-username']['input']
    username = escape_html(username.decode()).encode()
    password = form_data['login-password']['input']

    print(username, password)

    account_data = account_collection.find()
    for entry in account_data:
        # print(entry, flush=True)
        salt = entry["salt"]
        # print(salt, flush=True)
        encrypted_password = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password).digest()), salt)
        # print("encrypted")
        # print(encrypted_password, entry["password"])
        if entry["username"] == username and entry["password"] == encrypted_password:
            # print("account found")
            cookie = str(uuid.uuid4()).encode()
            hashed_cookie = hashlib.sha256(cookie).digest()
            # print(cookie, type(cookie), flush=True)
            account_collection.update_one({"username": username}, {'$set': {'cookie': hashed_cookie}})
            cookie = b'Set-Cookie: id=' + cookie + b'; Max-Age=3600; HttpOnly'
            # print(cookie, flush=True)
            # print(redirect("/", cookie), flush=True)
            handler.request.sendall(response_301("/", cookie))

    handler.request.sendall(response_301("/"))
