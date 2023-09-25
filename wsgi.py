from app import create_app
from flask import g
class AppVariable():
    def __init__(self):
        self._uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
        self._client = None
        self._user = None

app = create_app()
with app.app_context():
    g.application = AppVariable()
app.app_context().push()
