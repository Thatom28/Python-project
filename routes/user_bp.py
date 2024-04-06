from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models.users import User
from extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import login_user, login_required, logout_user
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash

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
        login_user(user)
        return render_template("dashboard.html", username=form.username.data)
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
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template("dashboard.html")
        except Exception as e:
            db.session.rollback()
            return f"<h1>Error happend {str(e)}</h1>", 500
    # if GET
    return render_template("register.html", form=form)


# -------------------------------------------------------------------------------------


def is_logged_in():
    return "id" in session


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_page"))
