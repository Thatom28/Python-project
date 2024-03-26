from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    render_template,
    session,
)

# from flask_login import UserMixin, login_user, login_required
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired
# from werkzeug.security import generate_password_hash, check_password_hash
# import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date


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


# LogIn page
@app.route("/login")
def login():
    # login_user()
    return render_template("login.html")


# method when the user submits a form
@app.route("/user/dashboard", methods=["POST"])
def user_logged_in():
    username = request.form.get("username")
    password = request.form.get("password")
    # verifying the  user
    # user = [user["name"] for user in users if user["name"] == username]
    # if user:
    #     return render_template("dashboard.html", username=username)
    # return render_template("register.html")
    return render_template("dashboard.html", username=username)


# profile page
# @app.route("/dashboard")
# def dashboard():
#     # tesla_df = pd.read_csv("tesla_stock_market_trends.csv")
#     # graph = plt.scatter(tesla_df["high"], tesla_df["date"])
#     return render_template("dashboard.html", my_policies=my_policies)


# @app.route("/add_new_policy", methods=["POST"])
# def add_new_policy():
#     policy_type = request.form["policy_type"]
#     policy_amount = request.form["policy_amount"]
#     if policy_type and policy_amount:
#         my_policies.append({"type": policy_type, "amount": policy_amount})
#     return redirect(
#         url_for("dashboard")
#     )  # Redirect to the dashboard route instead of rendering the template directly


# @app.post("/add_new_policy/<new_policy>")
# def add_new_policy(new_policy):
#     my_policies.append(new_policy)
#     return render_template("/add_policy.html")


# # takes us to the add_policy page
# @app.route("/add_policy", methods=["GET"])
# def add_policy():
#     return render_template("add_policy.html", policies=policies)


# show us a list of policies taken
# @app.route("/active_policies", methods=["POST"])
# def active_policies():
#     return render_template("active_policies.html", my_policies=my_policies)


# Policies page for the about page
@app.route("/policies")
def policies():
    return render_template("policies.html", policies=policies)


# Register page
@app.route("/register")
def register():
    return render_template("register.html")


# Adding the user to the users list
@app.post("/register")
def add_user():
    username = request.form.get(
        "username"
    )  # retriving the data from the from with the same name
    password = request.form.get("password")
    ids = [int(user["id"]) for user in users]
    largest_id = max(ids)
    new_user = {
        "CreatedAt": date.today(),
        "name": username,
        "password": password,
        "id": str(largest_id + 1),
    }
    users.append(new_user)
    return jsonify(new_user), 201


# @app.route("/my_policies", methods=["GET", "POST", "PUT", "DELETE"])
# def my_policies():
#     username = session.get("username")
#     if username():  # theu user found
#         user_data = users.get(username)
#         if user_data:
#             policies = user_data.get("policies")
#             return render_template(
#                 "my_policies.html", username=username, policies=policies
#             )


# calculator in te nav
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
    else:
        return render_template("calculation.html")


# calculations in  the add policy page| to display the qote on screen
@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        base_price = 50
        type_of_insurance = request.form.get("type")
        location = request.form.get("location")
        age = request.form.get("age")
        vehicle_model = request.form.get("vehicle_model")
        if location in high_risk_areas:
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


my_policies = [
    {
        "Insurance-type": "Home-Insurance",
        "createdAt": "2024-03-24T05:56:26.481Z",
    },
]
current_date = date.today()  # a fuction cannot be appended


# To add qoute/policy to the my_policy list and display my policy page
@app.route("/my_policies", methods=["POST", "Get"])
def my_policies():
    if request.method == "POST":
        type_of_insurance = request.form.get("type")
        location = request.form.get("location")
        age = request.form.get("age")
        vehicle_model = request.form.get("vehicle_model")
        new_policy = {
            "Insurance-type": type_of_insurance,
            "createdAt": date.today(),
        }
        my_policies.append(new_policy)
        return render_template("my_policies.html", my_policies=my_policies)
    return render_template("my_policies.html", my_policies=my_policies)


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


# @app.delete("/policies/<id>")  # <> converts to a variable
# def delete_policy(id):
#     policy = next(
#         (policy for policy in policies if policy["id"] == id), None
#     )  # the ers policy list
#     if policy:
#         policies.remove(policy)
#         return jsonify({"data": policy, "message": "policy deleted sucessfully"})
#     else:
#         result = {"message": "policy not found"}
#         return jsonify(result), 404


# @app.put("/policies/<id>")  # <> converts to a variable
# def update_policy(id):
#     updates = request.json  # get the data from json
#     policy = next(
#         (policy for policy in policies if policy["id"] == id), None
#     )  # find the movie id
#     if policy:
#         policy.update(updates)
#         return jsonify({"data": policy, "message": "policy updated sucessfully"})
#     else:
#         result = {"message": "policy not found"}
#         return jsonify(result), 404


# with open("policies.json", "w") as file:
#     json_data = json.dump(policies, file, indent=4)

if __name__ == "__main__":
    app.run(debug=True)  # to catch errors immediately
