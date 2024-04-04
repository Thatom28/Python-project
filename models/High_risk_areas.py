from extensions import db


class High_risk_areas(db.Model):
    __tablename__ = "High_risk_areas"
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    area_name = db.Column(db.String(255))
