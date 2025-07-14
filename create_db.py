from extensions import db, app
from models import User,Ad,Course

with app.app_context():
    db.create_all()