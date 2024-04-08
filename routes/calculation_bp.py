from flask import Blueprint, request, render_template, flash, send_file
import flask_login

# from models.High_risk_areas import High_risk_areas
from extensions import db
from models.user_cover import User_Cover
from datetime import datetime, date
from sqlalchemy import exists
from loguru import logger
import os

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
        vehicle_current_worth = request.form.get("vehicle_current_worth")
        cover_name = request.form.get("cover_name")
        cover_id = request.form.get("cover_id")
        risk_area = [area for area in high_risk_areas if area == location]
        currentYear = datetime.now().year
        if year_bought is not None:
            if risk_area:
                if year_bought - currentYear < 5:
                    base_price *= base_price * 0.5
                if vehicle_current_worth < 300_000:
                    base_price += 30
                if 18 <= age <= 25:
                    base_price *= 0.5
            elif (
                year_bought - currentYear < 5
                and risk_area
                or year_bought - currentYear < 5
                and vehicle_current_worth < 300_000
                or risk_area
                and 18 <= age <= 25
                or year_bought - currentYear < 5
                and 18 <= age <= 25
                or risk_area
                and vehicle_current_worth < 300_000
                or 18 <= age <= 25
                and vehicle_current_worth < 300_000
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
        new_cover = User_Cover(
            cover_name=cover_name,
            cover_id=cover_id,
            vehicle_model=vehicle_model,
            vehicle_current_worth=vehicle_current_worth,
            location=location,
            date=date.today(),
        )
        try:
            db.session.add(new_cover)
            db.session.commit()
            # users_cover = User_Cover.query.all()
            flash("Cover added successfully")
        except Exception as e:
            logger.error(f"Failed to add cover to database: {e}")
            db.session.rollback()  # Undo the change
            flash("Cover not added")
        return render_template(
            "quote.html",
            type_of_insurance=type_of_insurance,
            location=location,
            age=age,
            vehicle_model=vehicle_model,
            amount=base_price,
            cover_name=cover_name,
        )
    else:
        return render_template("add_policy.html")


# calculations in  the add policy page| to display the qote on screen
@calculation_bp.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        location = request.form["location"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        car_type = request.form["car_type"]
        driving_experience = int(request.form["driving_experience"])
        inflation_rate = float(request.form["inflation_rate"])

        base_premium_rate = 600

        if location in high_risk_areas:
            location_amount = 1.5
        else:
            location_amount = 1.0

        if age < 25:
            age_amount = 1.5  # Increase premium by 50% for age under 25
        elif age < 40:
            age_amount = 1.2  # Increase premium by 20% for age 25-39
        else:
            age_amount = 1.0  # No adjustment for age 40 and above

        if gender == "male":
            gender_amount = 1.5
        else:
            gender_amount = 1.0

        if car_type in luxury_cars:
            car_type_amount = 1.5
        else:
            car_type_amount = 1

        if driving_experience < 1:
            experience_amount = 1.3
        elif driving_experience < 5:
            experience_amount = 1.2
        else:
            experience_amount = (
                0.9  # decrease premium if you have more than 5 years experience
            )

        total_adjustment = (
            location_amount
            * age_amount
            * gender_amount
            * car_type_amount
            * experience_amount
        )
        total_premium = (
            base_premium_rate * total_adjustment * (1 + inflation_rate / 100)
        )

        return render_template(
            "quotation.html",
            location=location,
            gender=gender,
            age=age,
            car_type=car_type,
            driving_experience=driving_experience,
            total_premium=total_premium,
        )
    else:
        return render_template("calculation.html")


@calculation_bp.route("/download")
def download_file():
    # Specify the path to the file to be downloaded
    file_path = "Libraries\Documents"

    # Check if the file exists
    if os.path.exists(file_path):
        # Send the file as an attachment and open it in a new browser tab
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found"


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
luxury_cars = [
    "Mercedes-Benz S-Class",
    "BMW 7 Series",
    "Audi A8",
    "Lexus LS",
    "Porsche Panamera",
    "Jaguar XJ",
    "Bentley Continental GT",
    "Rolls-Royce Phantom",
    "Tesla Model S Plaid",
    "Cadillac CT6",
    "Lincoln Continental",
    "Maserati Quattroporte",
    "Aston Martin DB11",
    "Ferrari GTC4Lusso",
    "Lamborghini Aventador",
    "Bugatti Chiron",
    "McLaren 720S",
    "Bentley Flying Spur",
    "Genesis G90",
    "Karma Revero GT",
    "Acura RLX",
    "Infiniti Q70",
    # Add more luxury car models as needed
]

# Base premium rate
# base_premium_rate = 0.02  # 2% of car worth

# # Location-based adjustment
# if location in high_risk_areas:
#     location_adjustment = 1.5  # Increase premium by 50% if in high risk areas
# else:
#     location_adjustment = 1.0  # No adjustment for rural areas

# # Duration-based adjustment
# if duration_owned < 1:
#     duration_adjustment = 1.2  # Increase premium by 20% for less than 1 year ownership
# elif duration_owned < 5:
#     duration_adjustment = 1.0  # No adjustment for 1-4 years ownership
# else:
#     duration_adjustment = 0.8  # Decrease premium by 20% for 5 or more years ownership

# # Age-based adjustment
# if age < 25:
#     age_adjustment = 1.5  # Increase premium by 50% for age under 25
# elif age < 40:
#     age_adjustment = 1.2  # Increase premium by 20% for age 25-39
# elif age < 60:
#     age_adjustment = 1.0  # No adjustment for age 40-59
# else:
#     age_adjustment = 1.3  # Increase premium by 30% for age 60 and above

# # Calculate total premium
# total_premium = base_premium_rate * car_worth * location_adjustment * duration_adjustment * age_adjustment

# return total_premium
