from app import db
from PIL import Image
import base64
import io

class Request():
    def __init__(self):
        self.request = None
        self.respone = None
        self.status = None

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
        
        self.parsingIDRequest()
        self.connectIDImage()
    
    def parsingIDRequest(self):
        from app import db
        data = db.connectUserRequest()
        for item in data:
            if item["id"] == str(self.id):
                self.requests.append(item)
    
    def connectIDImage(self):
        from app import db
        self.image = db.connectUserImage(self.id)
    
    def parsingIDImage(self):
        try:
            self.image =  Image.open(io.BytesIO(base64.b64decode(self.image)))
        except Exception as e:
            print(e)
    
    def updateRequest(self):
        self.requests.clear()
        self.parsingIDRequest()
        

    
        

        