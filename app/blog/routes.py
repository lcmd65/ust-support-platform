from flask import Blueprint
from flask import request, render_template, redirect, url_for

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    import app
    return render_template("blog/home.html", app_username = app.application._user.username, app_image = app.application._user.image)


@home_blueprint.route("/home/chatbox", methods = ['GET', 'POST'])
def homeChatbox():
    pass


@home_blueprint.route("/home/chatbot", methods = ['GET', 'POST'])
def homeChatbot():
    pass 

@home_blueprint.route("/home/speechtotext", methods = ['GET', 'POST'])
def homeSpeechToText():
    pass 


