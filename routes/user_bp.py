from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    session,
    url_for,
    Flask,
)
from models.users import User
from extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import login_user, login_required, logout_user
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

user_bp = Blueprint("user_bp", __name__)


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
            user_data = user.to_dict()
            form_password = field.data
            print(f"Form passowrd is: {form_password}")
            if not check_password_hash(user_data["password"], form_password):
                raise ValidationError("Username or password incorrect")


@user_bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    # if post(when submit is clicked)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # session["username"] = request.form["username"]
        # session["logged_in"] = True
        username = request.form["username"]
        session["username"] = username
        login_user(user)
        return render_template("dashboard.html", username=session["username"])
    else:
        return render_template("login.html", form=form)


# --------------------------------------------------------------------------------------------------------------------------------
# Register
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    email = EmailField("Email", validators=[InputRequired()])
    date_of_birth = DateField("Date of Birth", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    gender = StringField("Gender", validators=[InputRequired()])
    mobile_number = StringField("Mobile Number", validators=[InputRequired()])
    submit = SubmitField("sign up")

    # to display something to the user if error occurs
    # Called automatically when the submit happens
    # field gets the data the user is submitting
    def validate_username(self, field):
        # check if they exist by the column name and teh data given on te for
        existing_username = User.query.filter_by(username=field.data).first()
        if existing_username:
            raise ValidationError("User name already exists")


# ---------------------------------------------------------------------------------
@user_bp.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    # if post(when submit is clicked)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        print(hashed_password, form.password.data)
        # get the user from the form
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            mobile_number=form.mobile_number.data,
            gender=form.gender.data,
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            # storing in session to access in other methods
            session["username"] = request.form.get("username")
            session["userid"] = request.form.get("userid")
            session["date_of_birth"] = request.form.get("date_of_birth")
            session["email"] = request.form.get("email")
            session["first_name"] = request.form.get("first_name")
            session["last_name"] = request.form.get("last_name")
            session["mobile_number"] = request.form.get("mobile_number")
            session["date_of_birth"] = request.form.get("date_of_birth")
            session["gender"] = request.form.get("gender")
            return render_template(
                "login.html",
                username=session["username"],
                first_name=session["first_name"],
                last_name=session["last_name"],
                mobile_number=session["mobile_number"],
                date_of_birth=session["date_of_birth"],
                gender=session["gender"],
            )
        except Exception as e:
            db.session.rollback()
            return f"<h1>Error happend {str(e)}</h1>", 500
    # if GET
    return render_template("register.html", form=form)


# -------------------------------------------------------------------------------------
@user_bp.route("/update_personal_info/<id>", methods=["POST", "GET"])
def update_personal_info(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.first_name = request.form.get("first_name", user.first_name)
        user.last_name = request.form.get("last_name", user.last_name)
        user.gender = request.form.get("gender", user.gender)
        user.username = request.form.get("username", user.username)
        user.date_of_birth = request.form.get("date_of_birth", user.date_of_birth)
        user.mobile_number = request.form.get("mobile_number", user.mobile_number)
        user.email = session.get("email", user.email)
        user.password = session.get("password", user.password)
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender,
            mobile_number=user.mobile_number,
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template(
                "dashboard.html",
                username=username,
                password=user.password,
                email=user.email,
                date_of_birth=user.date_of_birth,
                first_name=user.first_name,
                last_name=user.last_name,
                mobile_number=user.mobile_number,
                gender=user.gender,
            )
        except Exception as e:
            return f"{e}"
    else:
        username = session.get("username")
        print(session.get("username"))
        date_of_birth = session.get("date_of_birth")
        return render_template(
            "update_personal_info.html", username=username, date_of_birth=date_of_birth
        )


# def is_logged_in():
#     return "id" in session


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    # session.pop("logged_in", None)
    session["usersname"] = None
    return redirect(url_for("user_bp.login"))
