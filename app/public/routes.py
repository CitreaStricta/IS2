from flask import abort, render_template, url_for, redirect
from flask_login import current_user
from . import public_bp


@public_bp.route("/")
def index():
    if current_user.is_authenticated: # si esta autentificado
        if not current_user.is_admin:
            return redirect(url_for("surveys.MySurveys"))
        return render_template("public/index.html")

    else: return redirect(url_for("auth.login"))
