import requests
from flask import Flask, render_template, abort, request, jsonify
from flask import request, redirect, url_for
import codecs
import gensim
import external
from distutils.version import LooseVersion, StrictVersion
from packaging import version
from views import home
import os
import importlib

# Import the Flask app from the external module
external_app = importlib.import_module("external")



if __name__ == "__main__":
    external.word2vec_model = 'data/vnex.model.bin'
    external.app.run(port=8089)
