from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    flash,
    send_file,
    session,
    url_for,
)
from flask_login import current_user

# from models.High_risk_areas import High_risk_areas
from extensions import db
from models.user_cover import User_Cover
from datetime import datetime, date
import os
from models.claims import Claims


claim_bp = Blueprint("claim_bp", __name__)

user = current_user

print(user)


@claim_bp.route("/claims", methods=["GET"])
def claim():
    if request.method == "GET":
        # user_covers = User_Cover.query.filter(User_Cover.user_id == user.id).all()
        user_claims = Claims.query.filter(Claims.user_id == user.id).all()
        return render_template("claims.html", claims=user_claims)
    return render_template("claims.html", claims=user_claims)


@claim_bp.route("/claim/<id>", methods=["POST"])
def claim_cover(id):
    cover = User_Cover.query.get(id)
    if request.method == "POST":
        if cover:
            difference_in_days = (date.today() - cover.date).days

            difference_in_days_float = float(difference_in_days)

            payout_amount = difference_in_days_float * cover.premium_amount - 0.2
            print(f"this is the payout amount {payout_amount}")
            print(f"{cover.cover_id}covername{cover.cover_name}")
            try:
                new_entry = Claims(
                    user_id=cover.user_id,
                    user_cover_id=cover.id,
                    premium=cover.premium_amount,
                    Amount=payout_amount,
                    date=date.today(),
                    status="Pending",
                )
                print(f"{cover.cover_id}covername{cover.cover_name}")
                db.session.add(new_entry)
                db.session.commit()
                flash("Claim submitted to the agent!", "success")
                return render_template(
                    "claims.html",
                    claims=[new_entry],
                )
            except Exception as e:
                return f"<h1>Error happened {str(e)}</h1>", 500

        flash("Cover not found!", "error")
        return redirect(url_for("add_bp.rewards"))

    return render_template(
        "claims.html",
        claims=[cover],
        payout_amount=payout_amount,
        status="Pending",
    )
