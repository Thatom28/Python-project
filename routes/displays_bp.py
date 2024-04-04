from flask import Blueprint, render_template
from models.policies import Policies, Car_insurance

displays_bp = Blueprint("displays_bp", __name__)


# Policies page for the about page
@displays_bp.route("/policies")
def policies():
    policies = Policies.query.all()
    data = [policy.to_dict() for policy in policies]
    return render_template("policies.html", policies=data)


# Home page
@displays_bp.route("/")
def home():
    return render_template("home.html", policies=policies)


# -----------------------------------------------------------------------------------------------
# car insurance covers


@displays_bp.route("/car_insurance")
def car_insurance():
    car_insurances = Car_insurance.query.all()
    data = [car_insurance.to_dict() for car_insurance in car_insurances]
    return render_template("car_insurance.html", car_insurances=data)
