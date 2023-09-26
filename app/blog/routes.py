#blogging main function of nohdata
from flask import Blueprint
from flask import (
    request,
    render_template,
    redirect,
    url_for,
    g)
import app.cache
from app import db

home_blueprint = Blueprint('home_blueprint', __name__)
            

@home_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    user = app.cache.cache.get('database')
    if request.method == "POST":
        button_value = request.form.get("button")
        if button_value == "chatbox":
            return redirect("/chatbox")
        elif button_value == "chatbot":
            return redirect("/chatbot")
        else:
            return redirect("/speechtotext")
    return render_template("blog/home.html", app_username = user.username,\
        app_image = user._user.image)

@home_blueprint.route("/chatbox", methods = ['GET', 'POST'])
def homeChatbox():
    if request.method == "POST":
        tree = None
        button = None
        user = app.cache.cache.get('database')
        data_base = db.DB()
        data_base.getUser(user)
        id = request.form.get("option")
        for item in data_base._user.requests:
            if item["_id"] == id:
                tree = item
                break
        if tree != None:
            return render_template("blog/chatbox.html", user_name= data_base._user.username,\
            user_image = data_base._user.image,\
            tree_request = data_base._user.requests,\
            item_request = tree,\
            item_new = None)
        elif tree == None:
            button = request.form.get("button")
            if button == "init":
                return render_template("blog/chatbox.html", user_name= data_base._user.username,\
                user_image = data_base._user.image,\
                tree_request = data_base._user.requests,\
                item_request = None,\
                item_new = button)
    return render_template("blog/chatbox.html", user_name= data_base._user.username,\
            user_image = data_base._user.image,\
            tree_request = data_base._user.requests,\
            item_request = None,\
            item_new = None)
    
@home_blueprint.route("/chatbot", methods = ['GET', 'POST'])
def homeChatbot():
    return render_template("blog/chatbot.html")

@home_blueprint.route("/speechtotext", methods = ['GET', 'POST'])
def homeSpeechToText():
    return render_template("blog/speechtotext.html")


