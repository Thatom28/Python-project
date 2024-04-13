from flask import Blueprint, render_template
from models.policies import Policies, Car_insurance
from models.rewards import Rewards

displays_bp = Blueprint("displays_bp", __name__)


# Home page
@displays_bp.route("/")
def home():
    return render_template("home.html")


# Policies page for the about page
@displays_bp.route("/policies")
def policies():
    policies = Policies.query.all()
    data = [policy.to_dict() for policy in policies]
    return render_template("policies.html", policies=data)


# -----------------------------------------------------------------------------------------------
# car insurance covers


@displays_bp.route("/car_insurance")
def car_insurance():
    car_insurances = Car_insurance.query.all()
    data = [car_insurance.to_dict() for car_insurance in car_insurances]
    return render_template("car_insurance.html", car_insurances=data)


@displays_bp.route("/car_insurance_loggedin")
def car_insurance_loggedin():
    car_insurances = Car_insurance.query.all()
    data = [car_insurance.to_dict() for car_insurance in car_insurances]
    return render_template("car_insurance_loggedin.html", car_insurances=data)


@displays_bp.route("/car_insurance/<id>")  # HOF
def car_insurance_details(id):
    filtered_cover = Car_insurance.query.get(id)
    if filtered_cover:
        data = filtered_cover.to_dict()
        return render_template("cover_detail.html", policy=data)
    else:
        return "<h1>Policy not found</h1>"


@displays_bp.route("/rewards")
def rewards():
    rewards = Rewards.query.all()
    data = [reward.to_dict() for reward in rewards]
    return render_template("rewards.html", rewards=data)
