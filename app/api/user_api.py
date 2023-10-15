import flask
from flask import render_template, Blueprint, request
from app import db
from app.auth.models import User, dbModel
import json
from flask import jsonify
from app.blog.models import Conver


api_blueprint = Blueprint("api_blueprint", __name__)

## user api
@api_blueprint.route("/use_api", methods = ['POST'])
def user_api():
    try:
        import app.cache
        model = json.loads(app.cache.cache.get('database'))
        return jsonify(model.get["requests"])
    except Exception as e:
        # Handle the exception gracefully
        return jsonify(f"Failed to generate response: {e}")
    
# get cache request api
@api_blueprint.route("/openai_api", methods = ['POST'])
def openai_api():
    try:
        import app.cache
        message = request.json.get('message')
        if app.cache.cache.get["Conversation"] == None:
            conversation = Conver()
            conversation.addConver(message)
            app.cache.cache.set["Conversation"] = conversation
            return jsonify(conversation.getConver())
        else:
            conversation = app.cache.cache.get["Conversation"]
            conversation.addConver(message)
            return jsonify(conversation.getConver())
    except Exception as e:
        # Handle the exception gracefully
        return jsonify(f"Failed to generate response: {e}")
    
