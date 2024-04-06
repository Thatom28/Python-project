import uuid
from extensions import db


class Policies(db.Model):
    __tablename__ = "Policies"

    id = db.Column(
        db.String(50),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    cover = db.Column(db.String(255))
    premium = db.Column(db.Float)
    name = db.Column(db.String(255))
    short_description = db.Column(db.String(255))
    bonus = db.Column(db.String(255))
    image = db.Column(db.String(255))
    description = db.Column(db.String(350))

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "premium": self.premium,
            "short_description": self.short_description,
            "description": self.description,
            "image": self.image,
            "bonus": self.bonus,
        }


class Car_insurance(db.Model):
    __tablename__ = "Car_insurance"

    id = db.Column(
        db.String(50),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    cover_name = db.Column(db.String(255))
    cover_description = db.Column(db.String(255))
    base_price = db.Column(db.Float)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "cover_name": self.cover_name,
            "cover_description": self.cover_description,
            "base_price": self.base_price,
            "image_url": self.image_url,
        }
