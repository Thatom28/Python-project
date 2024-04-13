import uuid
from extensions import db


class Rewards(db.Model):
    __tablename__ = "Rewards"
    id = db.Column(
        db.String(50),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    rewards_image = db.Column(db.String(255))
    rewards_name = db.Column(db.String(50))
    rewards_description = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "rewards_image": self.rewards_image,
            "rewards_name": self.rewards_name,
            "rewards_description": self.rewards_description,
        }
