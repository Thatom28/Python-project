from flask import Blueprint, render_template
from app import User, db, RegistrationForm, LoginForm

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    # if post(when submit is clicked)
    if form.validate_on_submit():
        # get the user from the form
        # username = form.username.data
        # password = form.password.data
        new_user = User(username=form.username.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return "<h1>Registration successful"
        except Exception as e:
            db.session.rollback()
            return f"<h1>Error happend {str(e)}</h1>", 500
    # if GET
    return render_template("register.html", form=form)


# -------------------------------------------------------------------------------------


@user_bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    # if post(when submit is clicked)
    if form.validate_on_submit():
        return render_template("dashboard.html", username=form.username.data)
    else:
        return render_template("login.html", form=form)