import requests
import templates
#from flask import Flask, render_template, jsonify
from flask import Flask, render_template, abort, request, jsonify
from flask import request, redirect, url_for
import external

@external.app.route("/home/")
def homeView():
    return render_template("home.html")

@external.app.route("/login/",  methods = ['GETS'])
def loginView():
    return render_template("login.html")

