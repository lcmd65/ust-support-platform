from flask import Blueprint
from flask import request, render_template, redirect, url_for

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route("/home/",methods = ['GET', 'POST'])
def home():
    import app
    return render_template("blog/home.html", app_username = app.application._user.username, app_image =app.application._user.image)
    