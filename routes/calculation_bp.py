from flask import Blueprint, request, render_template
import flask_login

# from models.High_risk_areas import High_risk_areas
from extensions import db
from datetime import datetime
from sqlalchemy import exists
from loguru import logger

calculation_bp = Blueprint("calculation_bp", __name__)


# calculator in the nav
@calculation_bp.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        current_user = flask_login.current_user
        logger.info(f"Current user: {current_user}")
        base_price = 500
        type_of_insurance = request.form.get("type")
        location = request.form.get("location")
        age = int(request.form.get("age"))
        vehicle_model = request.form.get("vehicle_model")
        year_bought = request.form.get("year_bought")
        car_worth = request.form.get("car_worth")
        risk_area = [area for area in high_risk_areas if area == location]
        currentYear = datetime.now().year
        if year_bought is not None:
            if risk_area:
                if year_bought - currentYear < 5:
                    base_price *= base_price * 0.5
                if car_worth < 300_000:
                    base_price += 30
                if 18 <= age <= 25:
                    base_price *= 0.5
            elif (
                year_bought - currentYear < 5
                and risk_area
                or year_bought - currentYear < 5
                and car_worth < 300_000
                or risk_area
                and 18 <= age <= 25
                or year_bought - currentYear < 5
                and 18 <= age <= 25
                or risk_area
                and car_worth < 300_000
                or 18 <= age <= 25
                and car_worth < 300_000
            ):
                amount += base_price * 2.0
            elif risk_area:
                amount += base_price * 1.5
                location += "  (high risk area)"

            elif risk_area & 18 <= age <= 25:
                amount += base_price * 2.0
            elif 8 <= age <= 25:
                amount += base_price * 1.5
            elif year_bought - currentYear < 5:
                amount += base_price * 2.0

            selected_covers = request.form.get("")
            if age <= 18:
                return "<h2>minor : connot take an insurance</h2>"
            elif type_of_insurance == "car" and int(age) < 21:
                amount = base_price * 2
            else:
                amount = base_price
        return render_template(
            "quote.html",
            type_of_insurance=type_of_insurance,
            location=location,
            age=age,
            vehicle_model=vehicle_model,
            amount=base_price,
        )
    else:
        return render_template("add_policy.html")


# calculations in  the add policy page| to display the qote on screen
@calculation_bp.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        monthly_payments = int(request.form.get("monthly_payments"))
        no_of_years = int(request.form.get("no_of_years"))
        premium_payment = monthly_payments * (no_of_years * 3)

        return render_template(
            "quotation.html",
            monthly_payments=monthly_payments,
            no_of_years=no_of_years,
            premium_payment=premium_payment,
        )
    else:
        return render_template("calculation.html")


# ------------------------------------------------------------------------------------------------
high_risk_areas = [
    "cape town cbd",
    "joburg cbd",
    "durban cbd",
    "mitchells plain",
    "phoenic",
    "roodepoort",
    "mfuleni",
    "honey dew",
    "midrand",
    "hillbrow",
    "tembisa",
    "delf",
    "mamelodi",
    "hamanskraal",
    "braamfontein",
    "pretoria cbd",
    "rusternburg",
    "nyanga",
    "honeydew",
]
