import hashlib
import secrets
from database import xsrf_collection

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


def verifyXSRFToken(xsrf_token, account_collection):

    hashed_xsrf_token = hashlib.sha256(xsrf_token.encode()).digest()
    #doc = account_collection.find_one({"xsrf_token": hashed_xsrf_token})
    doc = account_collection.find_one({"xsrf_token": hashed_xsrf_token})

    if doc is not None:
        return True

    else:
        return False


def generateXSRFToken():

    token = secrets.token_urlsafe(32)
    return token
