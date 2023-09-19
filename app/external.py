from flask import Flask

app = Flask(__name__)
client = None
word2vec_model = None 


client = None # mongo client