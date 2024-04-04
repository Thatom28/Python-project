from flask import Blueprint, request, render_template

calculation_bp = Blueprint("calculation_bp", __name__)


# calculator in the nav
@calculation_bp.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        base_price = 50
        type_of_insurance = request.form.get("type")
        location = request.form.get("location")
        age = int(request.form.get("age"))
        vehicle_model = request.form.get("vehicle_model")

        selected_covers = request.form.get("")
        if age <= 18:
            return "<h2>minor : connot take an insurance</h2>"
        elif location in high_risk_areas:
            amount = base_price * 3
            location += "  (high risk area)"
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
            amount=amount,
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


# --------------------------------------------------------------------------------------
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
