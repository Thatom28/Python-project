import uuid
from extensions import db


class Claims(db.Model):
    __tablename__ = "Rewards"
    id = db.Column(
        db.String(50),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    rewardname = db.Column(db.String(255))
    Bonus = db.Column(db.String(255))
    cover_id = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "rewardname": self.rewardname,
            "cover_id": self.cover_id,
            "Bonus": self.Bonus,
        }
