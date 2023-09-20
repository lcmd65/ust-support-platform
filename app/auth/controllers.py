import app
from app.auth.models import User
from app.db import userParsing

def controlAuth(username, password):
    user_information = userParsing(username, password)
    app.application._user = User(user_information["username"], user_information["password"], user_information["email"], user_information["id"], user_information["gender"])
    

    
    