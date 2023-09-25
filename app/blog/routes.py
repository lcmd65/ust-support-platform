#blogging main function of nohg.application
from flask import Blueprint
from flask import (
    request,
    render_template,
    redirect,
    url_for,
    g)

home_blueprint = Blueprint('home_blueprint', __name__)
            

@home_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        button_value = request.form.get("button")
        if button_value == "chatbox":
            return redirect("/chatbox")
        elif button_value == "chatbot":
            return redirect("/chatbot")
        else:
            return redirect("/speechtotext")
    return render_template("blog/home.html", app_username = g.application._user.username,\
        app_image = g.application._user.image)

@home_blueprint.route("/chatbox", methods = ['GET', 'POST'])
def homeChatbox():
    if request.method == "POST":
        tree = None
        button = None
        id = request.form.get("option")
        for item in g.application._user.requests:
            if item["_id"] == id:
                tree = item
                break
        if tree != None:
            return render_template("blog/chatbox.html", user_name= g.application._user.username,\
            user_image = g.application._user.image,\
            tree_request = g.application._user.requests,\
            item_request = tree,\
            item_new = None)
        elif tree == None:
            button = request.form.get("button")
            if button == "init":
                return render_template("blog/chatbox.html", user_name= g.application._user.username,\
                user_image = g.application._user.image,\
                tree_request = g.application._user.requests,\
                item_request = None,\
                item_new = button)
    return render_template("blog/chatbox.html", user_name= g.application._user.username,\
            user_image = g.application._user.image,\
            tree_request = g.application._user.requests,\
            item_request = None,\
            item_new = None)
    
@home_blueprint.route("/chatbot", methods = ['GET', 'POST'])
def homeChatbot():
    return render_template("blog/chatbot.html")

@home_blueprint.route("/speechtotext", methods = ['GET', 'POST'])
def homeSpeechToText():
    return render_template("blog/speechtotext.html")


