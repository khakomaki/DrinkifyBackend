from flask import Flask
from app.firebase import init_firebase
from app.routes import api

def create_app():
    """
    Creates backend application
    """
    app = Flask(__name__)
    init_firebase(app)
    app.register_blueprint(api)
    return app
