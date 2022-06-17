<<<<<<< HEAD
from flask import abort, render_template, url_for
=======
from flask import abort, render_template, url_for, redirect
from flask_login import current_user
>>>>>>> develop
from . import public_bp


@public_bp.route("/")
def index():
<<<<<<< HEAD
    return render_template("public/index.html")
=======
    if current_user.is_authenticated: # si esta autentificado
        return render_template("public/index.html")
    else: return redirect(url_for("auth.login"))
>>>>>>> develop
