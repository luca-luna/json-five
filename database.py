from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client['312-Project']

user_collection = db['users']
user_id_collection = db['next_id']


def create_user_id():
    id = user_id_collection.find_one({})
    if id:
        next_id = int(id['prev_id']) + 1
        user_id_collection.update_one({}, {'$set': {'prev_id': next_id}})
        return next_id
    else:
        user_id_collection.insert_one({'prev_id': 1})
        return 1
