import uuid
from extensions import db


class Claims(db.Model):
    __tablename__ = "Claims"

    id = db.Column(
        db.String(255),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    user_id = db.Column(db.String(50))
    user_cover_id = db.Column(db.String(255))
    premium = db.Column(db.Float)
    Amount = db.Column(db.Float)
    date = db.Column(db.Date)
    status = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "cover_id": self.cover_id,
            "cover": self.cover,
            "amount": self.amount,
            "date": self.date,
            "status": self.status,
        }
