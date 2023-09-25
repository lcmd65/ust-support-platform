# authentication function of nohg.application
from flask import (\
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    current_app,
    g)
from app import db
from app.auth.models import User
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from app.auth.controllers import controlAuth
auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route("/login",  methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        link = g.application._uri
        g.application._client = MongoClient(link, server_api=ServerApi('1'))
        username = request.values['user'] 
        password = request.values['pass']
        bool = db.userAuthentication(username, password)
        if bool == True:
            controlAuth(username, password)
            return redirect("/home")
        else: 
            return render_template("auth/login.html", error="Invalid username or password.")
    return render_template('auth/login.html', error = error)

@auth_blueprint.route("/forgot",  methods = ['GET', 'POST'])
def forgotPassword():
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
    

@auth_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    try:
        if request.method == "POST":
            g.application._client = MongoClient(g.application._client._uri, server_api=ServerApi('1'))
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
    
@auth_blueprint.route("/base",  methods = ['GET','POST'])
def base():
    if request.method == "POST":
        button_name = request.form.get("button")
        if button_name == "login":
            return redirect('/login')
        elif button_name == "register":
            return redirect('/register')
    return render_template("base.html")
    

