from flask import Blueprint
from flask import request, render_template

my_blueprint = Blueprint('my_blueprint', __name__)
from app import db



@my_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    return render_template("blog/home.html")

@my_blueprint.route("/login",  methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.values['user'] 
        password = request.values['pass']
        bool = db.userAuthentication(username, password)
        if bool == True:
            return render_template("blog/home.html")
        else: 
            return \
            '''
                <form method="post">
                    <p><text = "login false">
                </form>
            '''
    return render_template('auth/login.html', error = error)

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
    


