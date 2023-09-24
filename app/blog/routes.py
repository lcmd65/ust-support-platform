#blogging main function of nohcel application
from flask import Blueprint
from flask import request, render_template, redirect, url_for

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    import app
    if request.method == "POST":
        button_value = request.form.get("button")
        if button_value == "chatbox":
            return redirect("/chatbox")
        elif button_value == "chatbot":
            return redirect("/chatbot")
        else:
            return redirect("/speechtotext")
    return render_template("blog/home.html", app_username = app.application._user.username,\
        app_image = app.application._user.image)


@home_blueprint.route("/chatbox", methods = ['GET', 'POST'])
def homeChatbox():
    import app
    return render_template("blog/chatbox.html", user_name= app.application._user.username,\
        user_image = app.application._user.image,\
        tree_request = app.application._user.requests)


@home_blueprint.route("/chatbot", methods = ['GET', 'POST'])
def homeChatbot():
    import app
    return render_template("blog/chatbot.html")

@home_blueprint.route("/speechtotext", methods = ['GET', 'POST'])
def homeSpeechToText():
    import app
    return render_template("blog/speechtotext.html")


