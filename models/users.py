from extensions import db
from flask_login import UserMixin
import uuid


class User(UserMixin, db.Model):
    # the table name to point to
    __tablename__ = "users"
    # add its columns                  #it will create random string for id| no need to add
    userid = db.Column(
        db.String(250), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "userid": self.userid,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
        }
