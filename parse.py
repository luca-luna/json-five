import hashlib
import secrets
from database import xsrf_collection, account_collection

def fileType(filename):

    file_type = filename[-4:]

    if "html" in file_type:
        return "html"
    elif "css" in file_type:
        return "css"
    elif "js" in file_type:
        return "javascript"
    elif "jpg" in file_type:
        return "jpg"


def verifyXSRFToken(xsrf_token, request):

    if xsrf_token == "" or hashlib.sha256("xsrf_token".encode()).digest() == "-1":
        return False

    hashed_xsrf_token = hashlib.sha256(xsrf_token.encode()).digest()
    #doc = account_collection.find_one({"xsrf_token": hashed_xsrf_token})
    doc = account_collection.find_one({"xsrf_token": hashed_xsrf_token})

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
    auth_cookie = hashlib.sha256(auth_cookie.encode()).digest()

    print("DOC:", doc, flush=True)
    if doc is not None and doc["cookie"] == auth_cookie:
        return True
    else:
        return False


def generateXSRFToken():

    token = secrets.token_urlsafe(32)
    return token
