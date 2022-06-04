<<<<<<< HEAD
from flask import abort, render_template
from . import public_bp

@public_bp.route("/")
def index():
    return render_template("public/home.html")
=======
from flask import abort, render_template, url_for
from . import public_bp


@public_bp.route("/")
def index():
    return render_template("public/index.html")
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
