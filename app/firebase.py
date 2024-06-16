import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase(app):
    """
    Initializes Firebase
    """
    # Get credentials from config file
    cred = credentials.Certificate("config.json")
    
    # Initialize app with service account
    firebase_admin.initialize_app(cred)

    app.config["FIRESTORE"] = firestore.client()
