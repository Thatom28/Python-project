from extensions import db


class User_Cover(db.Model):
    __tablename__ = "User_covers"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(255))
    username = db.Column(db.String(255))
    cover_id = db.Column(db.String(255))
    cover_name = db.Column(db.String(255))
    vehicle_model = db.Column(db.String(50))
    vehicle_current_worth = db.Column(db.Float)
    location = db.Column(db.String(50))
    date = db.Column(db.Date)
    # amount =

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "userid": self.userid,
            "username": self.username,
            "cover_id": self.cover_id,
            "cover_name": self.cover_name,
            "vehicle_model": self.vehicle_model,
            "vehicle_current_worth": self.vehicle_current_worth,
            "location": self.location,
            "date": self.date,
        }

    # def __repr__(self):
    #     return f"<User_Cover(user_id={self.user_id}, cover_id={self.cover_id})>"
