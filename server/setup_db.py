# server/setup_db.py

from server.app import create_app
from server.models import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
