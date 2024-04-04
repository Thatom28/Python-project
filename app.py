from flask import (
    Flask,
    request,
    render_template,
    render_template,
    redirect,
    url_for,
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
from extensions import db
from flask_login import LoginManager
from models.users import User


app = Flask(__name__)
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
# -----------------------------------------------------
from routes.user_bp import user_bp

app.register_blueprint(user_bp)

# --------------------------------------------------------
from routes.main_bp import main_bp

app.register_blueprint(main_bp)

# --------------------------------------------------------
from routes.calculation_bp import calculation_bp

app.register_blueprint(calculation_bp)

# ---------------------------------------------------------
from routes.displays_bp import displays_bp

app.register_blueprint(displays_bp)
# ------------------------------------------------------------------------------
from routes.add_bp import add_bp

app.register_blueprint(add_bp)


# verifys the user with this
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)  # to catch errors immediately
