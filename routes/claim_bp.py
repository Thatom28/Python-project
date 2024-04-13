from flask import Blueprint, request, render_template, flash, send_file, session
from flask_login import current_user

# from models.High_risk_areas import High_risk_areas
from extensions import db
from models.user_cover import User_Cover
from datetime import datetime, date
from sqlalchemy import exists
from loguru import logger
import os

claim_bp = Blueprint("claim_bp", __name__)

user = current_user


@claim_bp.route("/claim", methods=["POST", "GET"])
def claim():
    if request.method == "GET":
        # user_covers = User_Cover.query.filter(User_Cover.user_id == user.id).all()
        user_covers = User_Cover.query.filter(
            User_Cover.username == user.username
        ).all()
        return render_template("claims.html", user_covers=user_covers)
