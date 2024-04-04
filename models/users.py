from extensions import db
from flask_login import UserMixin
import uuid


class User(UserMixin, db.Model):
    # the table name to point to
    __tablename__ = "users"
    # add its columns                  #it will create random string for id| no need to add
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))
