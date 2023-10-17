from flask import render_template, Blueprint, request
from app import db
from app.auth.models import User, dbModel
import json
import openai
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
        from app.api.openai import api_getting
        openai.api_key = api_getting()
        message = request.json.get('message')
        if app.cache.cache.get("Conversation") == None:
            # create conversation cache
            conversation = Conver()
            conversation.addConver(message)
            output_message = conversation.getConver()
            app.cache.cache.set("Conversation",  json.dumps(conversation.__dict__()))
            return jsonify(output_message)
        else:
            # get conversation cache
            conversation_session = json.loads(app.cache.cache.get("Conversation"))
            conversation = Conver()
            conversation.bot_ = conversation_session["bot_"]
            conversation.user_ = conversation_session["user_"]
            conversation.score = conversation_session["score"]
            conversation.length = conversation_session["length"]
            conversation.output = conversation_session["output"]
            conversation.addConver(message)
            output_message = conversation.getConver()
            app.cache.cache.set("Conversation",  json.dumps(conversation.__dict__()))
            return jsonify(output_message)
    except Exception as e:
        # Handle the exception gracefully
        return jsonify(f"Failed to generate response: {e}")
    
