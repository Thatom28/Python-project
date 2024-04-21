from extensions import db
import uuid


class User_Cover(db.Model):
    __tablename__ = "User_rewards"
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(50), db.ForeignKey("Users.id"))
    Reward_id = db.column(db.String(50), db.ForeignKey("Reward_id"))
    rewards_image = db.Column(db.String(255))
    rewards_name = db.Column(db.String(50))
    rewards_description = db.Column(db.String(255))

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "user_id": self.user_id,
            "id": self.id,
            "rewards_image": self.rewards_image,
            "rewards_name": self.rewards_name,
            "rewards_description": self.rewards_description,
        }
