from flask import Blueprint, request, render_template, flash, send_file, session
import flask_login

# from models.High_risk_areas import High_risk_areas
from extensions import db
from models.user_cover import User_Cover
from datetime import datetime, date
from sqlalchemy import exists
from loguru import logger
import os

claim_bp = Blueprint("claim_bp", __name__)


@claim_bp.route("/claim", methods=["POST", "GET"])
def claim():
    if request.method == "GET":
        return render_template("claims.html")


@claim_bp.route("/rewards", methods=["POST", "GET"])
def rewards():
    if request.method == "GET":
        return render_template("rewards.html")
