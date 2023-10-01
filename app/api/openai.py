from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def api_getting():
    uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    db = client["Api"]
    collection = db["api"]
    documents = collection.find()
    api_key = None
    for item in documents:
        if item['api'] == 'nohcel-service':
            api_key = item['api-key']
            break
    return api_key
