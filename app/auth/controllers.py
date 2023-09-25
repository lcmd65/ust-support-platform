from app.auth.models import User
from app.db import userParsing
from flask import g

def controlAuth(username, password):
    user_information = userParsing(username, password)
    g.application._user = User(user_information["username"], user_information["password"], user_information["email"], user_information["id"], user_information["gender"])

    
    