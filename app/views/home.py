import requests
import templates
#from flask import Flask, render_template, jsonify
from flask import Flask, render_template, abort, request, jsonify
from flask import request, redirect, url_for
import external
import controls.database

@external.app.route("/home/",methods = ['GET', 'POST'])
def homeView():
    pass

@external.app.route("/login/",  methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.values['username'] 
        password = request.values['password']
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

