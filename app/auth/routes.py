from flask import Blueprint
from flask import request, render_template, redirect, url_for
from app import db
from app.auth.models import User
from app.auth.controllers import controlAuth

my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route("/login/",  methods = ['GET', 'POST'])
def login():
    import app
    error = None
    if request.method == "POST":
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
    return render_template("auth/forgot.html")
    

@my_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    try:
        error = None
        if request.method == "POST":
            username = request.values['user'] 
            password = request.values['pass']
            email = request.values['email'] 
            id = request.values['id']
            gender = request.values['gender']
    except:
        pass
    


