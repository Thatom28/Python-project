from flask import Flask
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os
from extensions import db
from flask_login import LoginManager
from models.users import User
from flask_session import Session

load_dotenv()  # load -> os env (enviroment variables)
# print(os.environ.get("AZURE_DATABASE_URL"), os.environ.get("FORM_SECRET_KEY"))

app = Flask(__name__)
# connection_string = os.environ.get("AZURE_DATABASE_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# Session(app)

connection_string = os.environ.get("LOCAL_DATABASE_URL")
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
# ----------------------------------------------------------
from routes.add_bp import add_bp

app.register_blueprint(add_bp)
# ------------------------------------------------------------
from routes.claim_bp import claim_bp

app.register_blueprint(claim_bp)


# verifys the user with this
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.drop_all()
        # db.create_all()
        print("creation done")
except Exception as e:
    print("Error connecting to the database:", e)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)  # to catch errors immediately
