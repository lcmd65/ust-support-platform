import requests
from flask import Flask, render_template, abort, request, jsonify
from flask import request, redirect, url_for
import codecs
import gensim
import external
from distutils.version import LooseVersion, StrictVersion
from packaging import version
from views.view import *
import os
import importlib
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Import the Flask app from the external module
external_app = importlib.import_module("external")
app = Flask(__name__, template_folder="templates")
uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"


if __name__ == "__main__":
    external.word2vec_model = 'data/vnex.model.bin'
    external.client = MongoClient(uri, server_api=ServerApi('1'))
    app.run(port=8089)
