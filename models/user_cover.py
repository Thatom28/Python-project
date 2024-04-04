from extensions import db


class User_Cover(db.Model):
    __tablename__ = "User_cover"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    cover_id = db.Column(db.Integer)

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "user_id": self.user_id,
            "cover_id": self.cover_id,
        }

    def __repr__(self):
        return f"<User_Cover(user_id={self.user_id}, cover_id={self.cover_id})>"
