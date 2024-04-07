from flask import Blueprint, render_template, request, flash, send_file
from extensions import db
from models.users import User
from models.user_cover import User_Cover
from models.policies import Car_insurance
from loguru import logger
from flask_wtf import FlaskForm

add_bp = Blueprint("add_bp", __name__)


# to display added policies
@add_bp.route("/user_covers", methods=["POST", "GET"])
def policy_taken():
    if request.method == "POST":
        logger.info("User has posted to /user_covers route")
        user_covers = User_Cover.query.all()
        return render_template("user_covers.html", user_covers=user_covers)

    else:
        user_covers = User_Cover.query.all()
        return render_template("user_covers.html", user_covers=user_covers)


# for the file upload
@add_bp.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        logger.success("File uploaded successfully")
        uploaded_file.save(uploaded_file.filename)
        return "File uploaded successfully!"
    else:
        return "No file selected!"


# Adding the policy to the db
@add_bp.route("/success")
def create_user_policy():
    cover_name = request.form.get("cover_name")

    new_cover = User_Cover(cover_name=cover_name)
    print(request.form.getlist("Accidents_cover"))
    try:
        db.session.add(new_cover)
        db.session.commit()
        flash("Cover added successfully")
        return render_template("user_covers.html")
    except Exception as e:
        db.session.rollback()  # Undo the change
        flash("Cover not added")
        return render_template("user_covers.html")


# --------------------------------------------------------
# CREATE A TABLE FOR THIS
@add_bp.route("/add_policy/<id>", methods=["GET", "POST"])
def add_policy(id):
    car_insurance = Car_insurance.query.get(id)
    if request.method == "GET":
        if car_insurance:
            return render_template("add_policy.html", car_insurance=car_insurance)
        else:
            return "<h1>Policy not found</h1>", 404
    else:
        # car_insurance.name = request.form.get('name') #add all columns
        # try and catch
        return render_template("add_policy.html")


@add_bp.route("/delete", methods=["POST"])
def delete_cover_by_id():
    filter_cover = User_Cover.query.get(id)
    if filter_cover:
        try:
            data = filter_cover.to_dict()
            db.session.delete(filter_cover)
            db.session.commit()
            flash("cover deleted")
            f"<h1>{data['name']} Movie deleted Successfully</h1>"
            return render_template(
                "user_covers.html",
            )
        except Exception as e:
            db.session.rollback()
            return str(e)
    else:
        flash("cover not found")
        return render_template("user_covers.html")


# ----------------------------------------------------------------
