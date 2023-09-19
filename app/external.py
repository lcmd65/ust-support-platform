from flask import Flask
app = Flask("main")
word2vec_model = None 


client = None # mongo client