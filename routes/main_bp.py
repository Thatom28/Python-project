from flask import Blueprint, render_template

main_bp = Blueprint("main_bp", __name__)


# About page
@main_bp.route("/about")
def about():
    return render_template("about.html")


# Contact page
@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


# after submitting contact form
@main_bp.route("/submitted")
def submitted():
    return render_template("submitted.html")
