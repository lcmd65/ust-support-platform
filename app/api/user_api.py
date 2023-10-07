import flask
from flask import render_template, Blueprint
from app import db
from app.auth.models import User, dbModel
import json
from flask import jsonify


api_blueprint = Blueprint("__name__")

## user api
@api_blueprint.route("/api", methods = ['POST'])
def user_api():
    try:
        import app.cache.cache
        model = json.loads(app.cache.cache.get('database'))
        return jsonify(model)
    except Exception as e:
        # Handle the exception gracefully
        return jsonify(f"Failed to generate response: {e}")