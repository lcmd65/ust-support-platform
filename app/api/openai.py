from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def api():
    uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    db = client["Api"]
    collection = db["api"]
    documents = collection.find()
    for item in documents:
        if item['api'] == 'nohcel-service':
            data = item['api-key']
            break
    api_key = data
    return api_key
