import base64
import io
from flask_caching import Cache
from PIL import Image
import app.cache
import json
        
class User():
    def __init__(self, username, password, email, ID, gender):
        self.username = username
        self.password = password
        self.email = email
        self.id = ID
        self.gender = gender
        self.image = None
        self.role = None
        self.requests = []
    
    def initFromUser(self, user):
        self.username = user['username']
        self.password = user['password']
        self.email = user['email']
        self.id = user['id']
        self.gender = user['gender']
        self.role = user['role']
        self.requests = user['requests']
        
class dbModel():
    def __init__(self, user):
        self.username = user.username
        self.password = user.password
        self.email = user.email
        self.id = user.id
        self.gender = user.gender
        self.role = user.role
        self.requests = user.requests
    
    def __dict__(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "id": self.id,
            "gender": self.gender,
            "role": self.role,
            "requests": self.requests,
        }
    

        

    
        

        