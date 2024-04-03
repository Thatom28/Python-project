from flask import (
    Flask,
    request,
    render_template,
    render_template,
    jsonify,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import matplotlib.pyplot as plt
import io
import base64


app = Flask(__name__)
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy()
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
db.init_app(app)


# table schema
class User(db.Model):
    # the table name to point to
    __tablename__ = "users"
    # add its columns                  #it will create random string for id| no need to add
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))


# --------------------------------------------------------------------------------------
# Policies
class Policies(db.Model):
    __tablename__ = "Policies"

    id = db.Column(
        db.String(50),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    name = db.column(db.String(255))
    cover = db.Column(db.String(255))
    premium = db.Column(db.Float)
    short_description = db.Column(db.String(255))
    description = db.Column(db.String(255))
    bonus = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "premium": self.premium,
            "short_description": self.short_description,
            "description": self.description,
            "image": self.image,
            "bonus": self.bonus,
        }


# Policies page for the about page
@app.route("/policies")
def policies():
    policies = Policies.query.all()
    data = [policy.to_dict() for policy in policies]
    return render_template("policies.html", policies=data)


# -----------------------------------------------------------------------------------------------
# car insurance covers
class Car_insurance(db.Model):
    __tablename__ = "Car_insurance"

    id = db.Column(
        db.String(50),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    cover_name = db.Column(db.String(255))
    cover_description = db.Column(db.String(255))
    base_price = db.Column(db.Float)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        # the name the front end wants the key to be
        return {
            "id": self.id,
            "cover_name": self.cover_name,
            "cover_description": self.cover_description,
            "base_price": self.base_price,
            "image_url": self.image_url,
        }


@app.route("/car_insurance")
def car_insurance():
    car_insurances = Car_insurance.query.all()
    data = [car_insurance.to_dict() for car_insurance in car_insurances]
    return render_template("car_insurance.html", car_insurances=data)


@app.route("/calculate", methods=["POST"])
def calculate_total():
    selected_covers = request.form.getlist(
        "cover"
    )  # Get the selected covers from the form
    # total_price = calculate_price(selected_covers)   # Calculate the total price
    # return render_template('result.html', total_price=total_price)
    print(selected_covers)


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        uploaded_file.save(uploaded_file.filename)
        return "File uploaded successfully!"
    else:
        return "No file selected!"


# --------------------------------------------------------------------------------------------------
class User_Cover(db.Model):
    __tablename__ = "User_cover"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    cover_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<User_Cover(user_id={self.user_id}, cover_id={self.cover_id})>"


# To add qoute/policy to the my_policy list and display my policy page
@app.route("/user_covers", methods=["POST", "Get"])
def policy_taken():
    if request.method == "POST":
        user_policies = db.session.query(User_Cover, User).join(User).all
        data = [user_cover.to_dict() for user_cover in user_policies]
        return render_template("user_covers.html", user_covers=data)
    else:
        user_policies = db.session.query(User_Cover, User).join(User).all()
        data = [user_cover.to_dict() for user_cover in user_policies]
        return render_template("user_covers.html", user_covers=data)


# --------------------------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log in")

    def validate_username(self, field):
        existing_username = User.query.filter_by(username=field.data).first()
        if not existing_username:
            raise ValidationError("Username or password incorrect")

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if user.password != field.data:
                raise ValidationError("Username or password incorrect")


# --------------------------------------------------------------------------------------------------------------------------------
# Register
class RegistrationForm(FlaskForm):
    # the fields (How they look on the template, the validators to the form)
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )

    submit = SubmitField("sign up")

    # to display something to the user if error occurs
    # Called automatically when the submit happens
    # field gets the data the user is submitting
    def validate_username(self, field):
        print("validate was called🤩🤩🤩🤩", field.data)
        # check if they exist by the column name and teh data given on te for
        existing_username = User.query.filter_by(username=field.data).first()
        if existing_username:
            raise ValidationError("User name already exists")


# --------------------------------------------------------------------------------------
# Home page
@app.route("/")
def home():
    return render_template("home.html", policies=policies)


# About page
@app.route("/about")
def about():
    return render_template("about.html")


# Contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")


# calculator in te nav
@app.route("/calculator", methods=["GET", "POST"])
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


# calculations in  the add policy page| to display the qote on screen
@app.route("/quote", methods=["GET", "POST"])
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


@app.route("/submitted")
def submitted():
    return render_template("submitted.html")


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

# methods to add, remove, update and delete insurances from the user profile
# @app.get("/policies")
# def get_policies():
#     return jsonify(policies)


# # # getting the policy by id
# @app.get("/policies/<id>")
# def get_policy_by_id(id):
#     policy = next((policy for policy in policies if policy["id"] == id), None)
#     if policy:
#         return jsonify(policy)
#     result = {"message": "User not found"}
#     return jsonify(result), 404


# @app.post("/policies")
# def add_policy():
#     new_policy = request.json  # get data from json
#     ids = [int(policy["id"]) for policy in policies]
#     largest_id = max(ids)
#     new_policy["id"] = str(largest_id + 1)  # add one to the max Id
#     policies.append(new_policy)
#     return jsonify({"data": new_policy, "message": "policy added succsefully"}), 201
# with open("policies.json", "w") as file:
#     json_data = json.dump(policies, file, indent=4)


from user_bp import user_bp

app.register_blueprint(user_bp)


# -------------------------------------------------------------------------------------
# Management (delete and edit)
# @app.delete("/<id>")
# def delete_policy(id):
#     # Permission to modify the lexical scope variable
#     filtered_policy = my_policies.query.get(id)
#     if not filtered_policy:
#         return jsonify({"message": "Policy not found"}), 404

#     try:
#         data = filtered_policy.to_dict()
#         db.session.delete(filtered_policy)
#         db.session.commit()  # Making the change (update/delete/create) permanent
#         return jsonify({"message": "Deleted Successfully", "data": data})
#     except Exception as e:
#         db.session.rollback()  # Undo the change
#         return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)  # to catch errors immediately
