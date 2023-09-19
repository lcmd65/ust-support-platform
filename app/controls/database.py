
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from models.user import User
from bson import ObjectId
import external
import os
import base64
import io
import requests
import mysql.connector
import time
import bson
from bson.binary import Binary


###### Mongo ####################################################################################################################################

uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
def getIPAddress():
    return requests.get("https://api.ipify.org").text

def addIPtoMongodbAtlas(ip_address):
    try:
        url = "https://cloud.mongodb.com/api/v1/admin/clusters/<CLUSTER_ID>/security/ipWhitelist/add"
        headers = {"Authorization": "Bearer <API_KEY>"}
        data = {"ipAddress": ip_address}
        response = requests.post(url, headers=headers, data=data)
    except Exception as e:
        print(e)
        
def getClient():
    external.client = MongoClient(uri, server_api=ServerApi('1'))

def connectMongoEmbedded():
    addIPtoMongodbAtlas(getIPAddress())
    # Send a ping to confirm a successful connection
    try:
        external.client.admin.command('ping')
        db = external.client["Nohcel_Dataset"]
        collection = db["embedded_dataset"]
        documents = collection.find()
        return documents
    except Exception as e:
        print(e)
     
## register user    
def addUserMongoDB(username, email, password, id , gender):
    getClient()
    external.client.admin.command('ping')
    db = external.client["User"]
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
def pushRequestToMongo(id, subject_text, request_text):
    document = {
            "_id": ObjectId(),
            "id": str(id),
            "subject": str(subject_text),
            "request": str(request_text),
            "respone": "",
        }
    db = external.client["User"]
    collection = db["Request"]
    collection.insert_one(document)
    return document

# return a request list 
def connectUserRequest():
    getClient()
    try:
        external.client.admin.command('ping')
        section_database = external.client["User"]
        collection_section = section_database["Request"]
        requests = collection_section.find()
        return requests
    except Exception as e:
        print(e) 
        
def userParsing(account,password):
    getClient()
    db = external.client["User"]
    collection = db["User_info"]
    documents = collection.find()
    for item in documents:
        if item["username"] == account and item["password"] == password:
            external.User_info = User(item["username"], item["password"], item["email"], item["id"], item["gender"])
        
def userAuthentication(account, password):
    external.client = MongoClient(uri, server_api=ServerApi('1'))
    addIPtoMongodbAtlas(getIPAddress())
    # Send a ping to confirm a successful connection
    external.client.admin.command('ping')
    db = external.client["User"]
    collection = db["User_info"]
    documents = collection.find()
    for item in documents:
        if item["username"] == account and item["password"] == password:
            return True
    return False
