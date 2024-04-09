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


# ------------------------------------------------------------------
@add_bp.route("/delete", methods=["POST"])
def delete_cover():
    print(f'The cover id is :{request.form.get("id")}')
    id = request.form.get("id")
    filter_cover = User_Cover.query.get(id)
    user_covers = User_Cover.query.all()
    if filter_cover:
        try:
            db.session.delete(filter_cover)
            db.session.commit()
            flash("cover deleted")
            user_covers = User_Cover.query.all()
            return render_template("user_covers.html", user_covers=user_covers)
        except Exception as e:
            db.session.rollback()
            return str(e)
    else:
        flash("cover not found")
        return render_template("user_covers.html")


# ----------------------------------------------------------------
@add_bp.route("/update/<id>", methods=["POST", "GET"])
def update_cover(id):
    cover = User_Cover.query.get(id)
    print(f"THE COVER ID IS == {User_Cover.query.get(id)}")
    if request.method == "GET":
        if cover:
            return render_template("edit_cover.html", cover=cover)
        else:
            return "<h1>Cover not found</h1>", 404
    else:
        if cover:
            cover.cover_id = request.form.get("cover_id", cover.cover_id)
            cover.cover_name = request.form.get("cover_name", cover.cover_name)
            cover.vehicle_model = request.form.get("vehicle_model", cover.vehicle_model)
            cover.vehicle_current_worth = request.form.get(
                "vehicle_current_worth", cover.vehicle_current_worth
            )
            cover.location = request.form.get("location", cover.location)
            cover.date = request.form.get("date", cover.date)
            try:
                db.session.commit()
                user_covers = User_Cover.query.all()
                return render_template("user_covers.html", user_covers=user_covers)
            except Exception as e:
                return f"<h1>Error happened {str(e)}</h1>", 500
        else:
            return f"<h1>Cover not found</h1>", 500
