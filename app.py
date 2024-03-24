from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    render_template,
    session,
)
from flask_login import UserMixin, login_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import json
import matplotlib.pyplot as plt
import pandas as pd


# class LoginForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Login")


app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("home.html", policies=policies)


# About page
@app.route("/about")
def about():
    return render_template("about.html", users=users)


# Contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")


def login_user():
    session["logged_in"] == True


def logout_user():
    session.pop("logged_in", None)


# LogIn page
@app.route("/login")
def login():
    # login_user()
    return render_template("login.html")


# profile page
@app.route("/profile")
def profile():
    tesla_df = pd.read_csv("tesla_stock_market_trends.csv")
    graph = plt.scatter(tesla_df["high"], tesla_df["date"])

    return render_template("profile.html", graph=graph)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = user.query.filter_by(username=form.username.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user)
#             return redirect(url_for("/home"))
#         else:
#             flash("Invalid username or password", "error")
#     return render_template("login.html", form=form)


# Policies page
@app.route("/policies")
def policies():
    return render_template("policies.html", policies=policies)


# Policies page
@app.route("/register")
def register():
    return render_template("register.html")


# Adding the user to the users list
@app.post("/register")
def add_user():
    new_user = request.json  # get data from json
    ids = [int(user["id"]) for user in users]
    largest_id = max(ids)
    new_user["id"] = str(largest_id + 1)  # add one to the max Id
    users.append(new_user)
    return jsonify(new_user), 201


@app.route("/my_policies", methods=["GET", "POST", "PUT", "DELETE"])
def my_policies():
    username = session.get("username")
    if username():  # theu user found
        user_data = users.get(username)
        if user_data:
            policies = user_data.get("policies")
            return render_template(
                "my_policies.html", username=username, policies=policies
            )


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        monthly_payments = int(request.form.get("monthly_payments"))
        no_of_years = int(request.form.get("no_of_years"))

        premium_payment = monthly_payments * (no_of_years * 3)
        return render_template(
            "quotation.html",
            monthly_paynemts=monthly_payments,
            no_of_years=no_of_years,
            premium_payment=premium_payment,
        )
    return render_template("calculation.html")


users = [
    {
        "createdAt": "2024-03-24T04:10:52.579Z",
        "name": "Ruby Hane",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/1076.jpg",
        "password": "Buckinghamshire",
        "id": "1",
    },
    {
        "createdAt": "2024-03-24T07:04:31.288Z",
        "name": "Dr. Peggy Shields",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/656.jpg",
        "password": "Coordinator",
        "id": "2",
    },
    {
        "createdAt": "2024-03-23T20:27:51.901Z",
        "name": "Joel McDermott",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/1083.jpg",
        "password": "Gasoline",
        "id": "3",
    },
    {
        "createdAt": "2024-03-24T05:56:26.481Z",
        "name": "Darla Klein",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/61.jpg",
        "password": "withdrawal",
        "id": "4",
    },
    {
        "createdAt": "2024-03-23T13:37:53.281Z",
        "name": "Connie Daniel",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/330.jpg",
        "password": "firewall",
        "id": "5",
    },
    {
        "createdAt": "2024-03-24T03:00:13.021Z",
        "name": "Dr. Maureen Altenwerth",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/26.jpg",
        "password": "Hybrid",
        "id": "6",
    },
    {
        "createdAt": "2024-03-23T14:03:03.780Z",
        "name": "Lucia Ondricka",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/171.jpg",
        "password": "Southeast",
        "id": "7",
    },
    {
        "createdAt": "2024-03-23T23:39:56.821Z",
        "name": "Mildred Schroeder PhD",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/849.jpg",
        "password": "Buckinghamshire",
        "id": "8",
    },
    {
        "createdAt": "2024-03-24T07:51:15.092Z",
        "name": "Ms. Cristina Beer",
        "avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/833.jpg",
        "password": "Northwest",
        "id": "9",
    },
]

policies = [
    {
        "cover": 6,
        "premium": 12,
        "name": "Life Cover",
        "short_description": "Secure Your Legacy, Protect Your Loved Ones",
        "Bonus": "grey",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": "We ease the burdern on your family should you die unexpectedly by paying once-off tax-free amout that can be used to cover their expenses for now and the future.",
        "id": "1",
    },
    {
        "cover": 1,
        "premium": 82,
        "name": "car Insurance",
        "short_description": "Safeguarding Your Drive",
        "Bonus": "Investment",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": "Hit the road with confidence knowing that your journey is protected by our comprehensive car insurance. From daily commutes to cross-country adventures, our coverage keeps you and your vehicle secure against life's unexpected twists and turns.",
        "id": "2",
    },
    {
        "cover": 51,
        "premium": 97,
        "name": "Home Insurance",
        "short_description": "Safeguarding Every Brick in Your Haven",
        "Bonus": "Metal",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": "Protecting your home is more than just safeguarding a structure—it's safeguarding your sanctuary, your memories, and your peace of mind, our home insurance coverage ensures that your home is shielded against life's uncertainties, whether it's fire, theft, or natural disasters. ",
        "id": "3",
    },
    {
        "cover": 59,
        "premium": 8,
        "name": "Business Insurance",
        "short_description": "Securing Your Sucess",
        "Bonus": "application",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": "we understand that your business is more than just a venture—it's your livelihood, your passion, and your legacy. That's why we offer comprehensive business insurance solutions designed to protect every aspect of your enterprise.",
        "id": "4",
    },
    {
        "cover": 22,
        "premium": 68,
        "name": "Retiremnet Annuity",
        "short_description": "Nurturing Security for Your Future",
        "Bonus": "Rutherfordium",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": " We understand the importance of planning for your future, especially during retirement. Our retirement annuity options offer a path to financial security, allowing you to enjoy the fruits of your labor with confidence. ",
        "id": "5",
    },
    {
        "cover": 42,
        "premium": 31,
        "name": "Short-term Insurance",
        "short_description": "Safeguard Your Adventures, Insure Your Thrills",
        "Bonus": "sternly",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": "Whether you're hitting the slopes, embarking on a road trip, or trying out a new extreme sport, our short-term insurance has you covered. Enjoy peace of mind knowing that your fun activities are protected against unexpected mishaps.  Explore worry-free",
        "id": "6",
    },
    {
        "cover": 3,
        "premium": 23,
        "name": "Agriculture Insurance",
        "short_description": "Harvesting Security, Cultivating Success",
        "Bonus": "City",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": "Despite modern techniques, there are still numerous risks and challenges facing farmers and their crops. As your partner in agriculture, we understand that effective risk management is crucial. We offer more than insurance expertise, we do our research to advise on growth effectiveness.",
        "id": "7",
    },
    {
        "cover": 49,
        "premium": 11,
        "name": "Income Protection",
        "short_description": "Cover for when you can't work",
        "Bonus": "ha",
        "image": "https://www.idfcfirstbank.com/content/dam/idfcfirstbank/images/blog/importance-of-having-savings-717x404.jpg",
        "description": "covers you and your family if you lose your income due to permanent or temporary disability or illness, by paying you a monthly income that allows you to maintain your standard of living.",
        "id": "8",
    },
]


# # getting all users
# @app.get("/users")
# def get_users():
#     return jsonify(users)


# # getting the user by id
# @app.get("/users/<id>")
# def get_user_by_id(id):
#     user = next((user for user in users if user["id"] == id), None)
#     if user:
#         return user
#     result = {"message": "User not found"}
#     return jsonify(result), 404


# # Creating a user from
# @app.post("/users")
# def create_user():
#     new_user = request.json  # get the data from json
#     ids = [int(user["id"]) for user in users]
#     largest_id = max(ids)
#     new_user["id"] = largest_id + 1
#     users.append(new_user)
#     result = {"message": "user added succesfully"}
#     return jsonify(result)


# # deleting a user
# @app.delete("/users/<id>")
# def delete_user_by_id(id):
#     user = next((user for user in users if user["id"] == id), None)
#     if user:
#         users.remove(user)
#         return jsonify({"data": user, "message": "User deleted successfully"})
#     return jsonify({"message": "user not found"})


# # editing the user
# @app.put("/users/<id>")
# def update_user(id):
#     updates = request.json
#     user = next((user for user in users if user["id"] == id), None)
#     if user:
#         user.update(updates)
#         return jsonify({"data": user, "message": "User updated successfully"})
#     else:
#         return jsonify({"message": "User not found"}), 404


# methods to add, remove, update and delete insurances from the user profile
@app.get("/policies")
def get_policies():
    return jsonify(policies)


# # getting the policy by id
@app.get("/policies/<id>")
def get_policy_by_id(id):
    policy = next((policy for policy in policies if policy["id"] == id), None)
    if policy:
        return jsonify(policy)
    result = {"message": "User not found"}
    return jsonify(result), 404


@app.post("/policies")
def Add_policy():
    new_policy = request.json  # get data from json
    ids = [int(policy["id"]) for policy in policies]
    largest_id = max(ids)
    new_policy["id"] = str(largest_id + 1)  # add one to the max Id
    policies.append(new_policy)
    return jsonify({"data": new_policy, "message": "policy added succsefully"}), 201


@app.delete("/policies/<id>")  # <> converts to a variable
def delete_policy(id):
    policy = next(
        (policy for policy in policies if policy["id"] == id), None
    )  # the ers policy list
    if policy:
        policies.remove(policy)
        return jsonify({"data": policy, "message": "policy deleted sucessfully"})
    else:
        result = {"message": "policy not found"}
        return jsonify(result), 404


@app.put("/policies/<id>")  # <> converts to a variable
def update_policy(id):
    updates = request.json  # get the data from json
    policy = next(
        (policy for policy in policies if policy["id"] == id), None
    )  # find the movie id
    if policy:
        policy.update(updates)
        return jsonify({"data": policy, "message": "policy updated sucessfully"})
    else:
        result = {"message": "policy not found"}
        return jsonify(result), 404


# with open("policies.json", "w") as file:
#     json_data = json.dump(policies, file, indent=4)

if __name__ == "__main__":
    app.run(debug=True)  # to catch errors immediately


# A user mdel that represent the users in the system
# class User(UserMixin, users):  # replace users with the database
#     for user in users:
#         id = user.id
#         username = user.name
#         password_hash = user.password

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
