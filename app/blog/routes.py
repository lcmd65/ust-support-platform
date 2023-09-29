#blogging main function of nohdata
from flask import Blueprint
from flask import (
    request,
    render_template,
    redirect,
    url_for,
    g)
import app.cache
import json
import openai
from app import db
from app.auth.models import User, dbModel

home_blueprint = Blueprint('home_blueprint', __name__)
            

@home_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    model = json.loads(app.cache.cache.get('database'))
    user = User(None, None, None, None, None)
    user.initFromUser(model)
    if request.method == "POST":
        button_value = request.form.get("button")
        if button_value == "chatbox":
            return redirect("/chatbox")
        elif button_value == "chatbot":
            return redirect("/chatbot")
        else:
            return redirect("/speechtotext")
    return render_template("blog/home.html", app_username = user.username,\
        app_image = user.image)

@home_blueprint.route("/chatbox", methods = ['GET', 'POST'])
def homeChatbox():
    tree = None
    button = None
    model = json.loads(app.cache.cache.get('database'))
    user = User(None, None, None, None, None)
    user.initFromUser(model)
    data_base = db.DB()
    data_base.getUser(user)
    if request.method == "POST":
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
    
@home_blueprint.route("/api", methods = ['POST'])
def api():
    from app.api.openai import api
    try:
        key = api()
        openai.api_key = key
        message = request.json.get("message")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        if completion.choices[0].message!=None:
            return completion.choices[0].messages
        else :
            return 'Failed to Generate response!'
    except:
        return 'Failed to Generate response!'

@home_blueprint.route("/chatbot", methods = ['GET', 'POST'])
def homeChatbot():
    return render_template("blog/chatbot.html")

@home_blueprint.route("/speechtotext", methods = ['GET', 'POST'])
def homeSpeechToText():
    return render_template("blog/speechtotext.html")


