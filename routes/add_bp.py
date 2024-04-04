from flask import Blueprint, render_template, request, flash
from extensions import db
from models.users import User
from models.user_cover import User_Cover

add_bp = Blueprint("add_bp", __name__)


# to display added policies
@add_bp.route("/user_covers", methods=["POST", "Get"])
def policy_taken():
    if request.method == "POST":
        user_policies = db.session.query(User_Cover, User).all()
        data = [user_cover.to_dict() for user_cover, _ in user_policies]
        return render_template("user_covers.html", user_covers=data)
    else:
        user_policies = db.session.query(User_Cover).all()
        data = [user_cover.to_dict() for user_cover, _ in user_policies]
        return render_template("user_covers.html", user_covers=data)


# for the file upload
@add_bp.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        uploaded_file.save(uploaded_file.filename)
        return "File uploaded successfully!"
    else:
        return "No file selected!"


# Adding the policy to the db
@add_bp.route("/success")
def create_user_policy():
    data = {"cover_name": request.form.get("cover_name")}
    new_cover = User_Cover(**data)
    try:
        db.session.add(new_cover)
        db.session.commit()
        flash("Cover added successfully")
        return render_template("user_covers.html")
    except Exception as e:
        db.session.rollback()  # Undo the change
        flash("Cover not added")
        return render_template("user_covers.html")
