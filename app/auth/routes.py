import requests
import templates
#from flask import Flask, render_template, jsonify
from flask import Flask, render_template, abort, request, jsonify
from flask import request, redirect, url_for
from main import app
import external
import controls.database

@app.route('/')
def main_view():
    return redirect('/login/')

@app.route("/home/",methods = ['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/login/",  methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.values['user'] 
        password = request.values['pass']
        bool = controls.database.userAuthentication(username, password)
        if bool == True:
            return render_template("home.html")
        else: 
            return \
            '''
                <form method="post">
                    <p><text = "login false">
                </form>
            '''
    return render_template('login.html', error = error)

@app.route("/register/", methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == "POST":
        username = request.values['user'] 
        password = request.values['pass']
        email = request.values['email'] 
        id = request.values['id']
        gender = request.values['gender']


