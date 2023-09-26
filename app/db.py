
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from .auth.models import User
import base64
from flask_caching import Cache
from bson.binary import Binary
from PIL import Image
import io

###### Mongo ####################################################################################################################################

class DB:
    def __init__(self):
        self._uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
        self._client = None
        self._user = None
        self.getClient()
    
    def getClient(self):
        self._client = MongoClient(self._uri, server_api=ServerApi('1'))
        
    def getUser(self, user):
        self._user = user
        
    def parsingUser(self):
        self.userParsing()
        self.parsingIDRequest()
        self.connectIDImage()

    
    def parsingIDRequest(self):
        data = self.connectUserRequest()
        for item in data:
            if item["id"] == str(self._user.id):
                self._user.requests.append(item)
    
    def connectIDImage(self):
        self._user.image = self.connectUserImage(self._user.id)
    
    def parsingIDImage(self):
        try:
            self._user.image =  Image.open(io.BytesIO(base64.b64decode(self.image)))
        except Exception as e:
            print(e)
    
    def updateRequest(self):
        self.requests.clear()
        self.parsingIDRequest()

    def connectMongoEmbedded(self):
        # Send a ping to confirm a successful connection
        try:
            self._client.admin.command('ping')
            db = self._client["Nohcel_Dataset"]
            collection = db["embedded_dataset"]
            documents = collection.find()
            return documents
        except Exception as e:
            print(e)
        
    ## register user    
    def addUserMongoDB(self, username, email, password, id , gender):
        self.getClient()
        self._client.admin.command('ping')
        db = self._client["User"]
        ## processing User basic infomation
        collection = db["User_info"]
        user = collection.find()
        for item in user:
            if item["id"] == id or item['username'] == username:
                return False
        try:
            document = {
                    "_id":ObjectId(),
                    "username": str(username),
                    "password": str(password),
                    "email": str(email),
                    "gender": str(gender),
                    "id": int(id),
                }
            collection.insert_one(document) 
            ## processing User image 
            collection_image = db["Image"]
            document_image = {
                "_id":ObjectId(),
                "id": int(id),
                "image": Binary(base64.b64encode(b'None'), 0),
            }
            collection_image.insert_one(document_image)
        except Exception as e: print(e)
        return True   

    # add request to mongo in chatbox
    def pushRequestToMongo(self, id, subject_text, request_text):
        document = {
                "_id": ObjectId(),
                "id": str(id),
                "subject": str(subject_text),
                "request": str(request_text),
                "respone": "",
            }
        db = self._client["User"]
        collection = db["Request"]
        collection.insert_one(document)
        return document

    # return a request list 
    def connectUserRequest(self):
        self.getClient()
        try:
            self._client.admin.command('ping')
            section_database = self._client["User"]
            collection_section = section_database["Request"]
            requests = collection_section.find()
            return requests
        except Exception as e:
            print(e) 
            
    def userParsing(self, account, password):
        self.getClient()
        db = self._client["User"]
        collection = db["User_info"]
        documents = collection.find()
        for item in documents:
            if item["username"] == account and item["password"] == password:
                self._user = User(item["username"], item["password"], item["email"], item["id"], item["gender"])
            
    def userAuthentication(self, account, password):
        # Send a ping to confirm a successful connection
        self._client.admin.command('ping')
        db = self._client["User"]
        collection = db["User_info"]
        documents = collection.find()
        for item in documents:
            if item["username"] == account and item["password"] == password:
                return True
        return False

    def connectUserImage(self, id):
        db = self._client["User"]
        collection = db["Image"]
        documents = collection.find()
        for item in documents:
            if str(item["id"]) == str(id):
                return item["image"]
            
    def userAuthenticationChange(self, account, email, password):
        # Send a ping to confirm a successful connection
        self._client.admin.command('ping')
        db = self._client["User"]
        collection = db["User_info"]
        documents = collection.find()
        for item in documents:
            if item["username"] == account and item["email"] == email:
                collection.update_one({"_id": item["_id"]}, {"password": password})
                return True
        return False
                
            
##### combine MySQL and MongoDB in Program Processing#########################################################################################
