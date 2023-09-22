from flask import Blueprint
from flask import request, render_template, redirect, url_for
from app import db
from app.auth.models import User
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from app.auth.controllers import controlAuth

my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route("/login/",  methods = ['GET', 'POST'])
def login():
    import app
    error = None
    if request.method == "POST":
        app.application._client = MongoClient(app.application._uri, server_api=ServerApi('1'))
        username = request.values['user'] 
        password = request.values['pass']
        bool = db.userAuthentication(username, password)
        if bool == True:
            app.application_user = controlAuth(username, password)
            return redirect("/home")
        else: 
            return render_template("auth/login.html", error="Invalid username or password.")
    return render_template('auth/login.html', error = error)

@my_blueprint.route("/forgot/",  methods = ['GET', 'POST'])
def forgotPassword():
    import app
    error = None
    if request.method == "POST":
        username = request.values['user'] 
        email = request.values['email']
        new_pass = request.values['new_password']
        confirm_pass = request.values['confirm_new_password']

        if new_pass == confirm_pass:
            boolean = db.userAuthenticationChange(username,email, new_pass)
            if boolean == True:
                return render_template("auth/forgot.html", error="Success change")
        else: 
            return render_template("auth/forgot.html", error="Wrong username or email")
    return render_template("auth/forgot.html", error = error)
    

@my_blueprint.route("/register/", methods = ['GET', 'POST'])
def register():
    try:
        import app
        if request.method == "POST":
            app.application._client = MongoClient(app.application._client._uri, server_api=ServerApi('1'))
            username = request.values['user'] 
            password = request.values['pass']
            confirm_password = request.values['confirm_password']
            email = request.values['email'] 
            id = request.values['id']
            gender = request.values['gender']
            if confirm_password == password:
                boolean = db.addUserMongoDB(username, email, password, id , gender)
                if boolean == True:
                    return render_template("auth/register.html", error = "Success")
                else:   
                    return render_template("auth/register.html", error = "Can't register new user")   
        return render_template("auth/register.html", error = None)
    except Exception as e:
        return render_template("auth/register.html", error = e)
    


