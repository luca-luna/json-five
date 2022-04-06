from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client['312-Project']

user_collection = db['users']
user_id_collection = db['next_id_users']

username_posted_collection = db['username']

message_collection = db['messages']
message_id_collection = db['next_id_messages']

dm_collection = db['dms']
dm_id_collection = db['next_id_dms']


'''
message_collection is for the homepage messaging area
this just stores the messages and the usernames associated w them

dm_collection is for the dms
this stores the messages and the usernames of both participants
'''


def create_id(collection):
    id = collection.find_one({})
    if id:
        next_id = int(id['prev_id']) + 1
        collection.update_one({}, {'$set': {'prev_id': next_id}})
        return next_id
    else:
        collection.insert_one({'prev_id': 1})
        return 1



def addHomepageMessage(info):

    id = create_id(message_id_collection)

    info["id"] = id

    message_collection.insert_one(info)

    created_record = message_collection.find_one({"id": id})
    del created_record["_id"]

    return created_record



def addDM(info):

    id = create_id(dm_id_collection)

    info["id"] = id

    dm_collection.insert_one(info)

    created_record = dm_collection.find_one({"id": id})
    del created_record["_id"]

    return created_record



def listHomepageMessages():

    docs = []
    for doc in message_collection.find({}):
        del doc["_id"]
        docs.append(doc)

    return docs



def listDMs(username1, username2):

    docs = []
    for doc in dm_collection.find( { "$or": [ { "username1": username1, "username2": username2}, {"username1": username2, "username2": username1} ] }):
        del doc["_id"]
        docs.append(doc)

    return docs












