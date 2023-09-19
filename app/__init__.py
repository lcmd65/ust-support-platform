
from flask import Flask, redirect, render_template, jsonify
import logging
import logging.handlers
from .extensions import *


def create_app():
    """Initiate flask app"""
    app = Flask(__name__, instance_relative_config=True, static_folder="static", template_folder="templates")
    app.config.from_pyfile('config.py')

    # login
    handler = logging.handlers.RotatingFileHandler(app.config["LOG_FILE"], maxBytes=app.config["LOG_SIZE"])
    handler.setLevel(app.config["LOG_LEVEL"])
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s [%(pathname)s at %(lineno)s]: %(message)s", "%Y-%m-%d %H:%M:%S"))
    app.logger.addHandler(handler)

    # init flask-extensions
    cors.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)

    with app.app_context():
        # TODO - register your blueprints here
        from .auth.routes import auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .auth.routes import auth_api_blueprint
        app.register_blueprint(auth_api_blueprint)
        csrf.exempt(auth_api_blueprint)

        # finally generate tables as per models
        db.create_all()

        # register common views
        @app.route("/")
        def home():
            """Handle root resource request"""
            return redirect("/login/")

        @app.errorhandler(404)
        def page_not_found(e):
            """Handle error gracefully"""
            return jsonify({"msg": "Resource not found. Visit API docs for more info.", "type": "+OK", "return": None})
            # return render_template("404.html"), 404

        @app.errorhandler(500)
        def internal_server_error(e):
            """Handle internal server error gracefully"""
            return jsonify({"msg": "Internal server error. Please contact support.", "type": "+OK", "return": None})
            # return render_template("500.html"), 500

    return app