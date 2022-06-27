from flask import render_template, redirect, url_for, request,abort
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User
from functools import wraps

@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        print(name,email,password)
        user = User.select_user(email)
        
        if user is None:
            # Creamos el usuario y lo guardamos
            user = User(name,email, password)
            user.set_password(password)
            user.insert_user()
            #Lo dejamos logeado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
        else: 
            error = f'El email {email} ya está siendo utilizado por otro usuario'
    return render_template("auth/signup_form.html", form=form, error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data

        user = User.select_user(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
        else:
            error = f'Datos incorrectos, intentelo nuevamente'
    return render_template('auth/login_form.html', form=form,error=error)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(email):
    return User.get_by_email(email)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
        return f(*args, **kws)
    return decorated_function

#def login_required(is_admin="ANY"):
#    def wrapper(fn):
#        @wraps(fn)
#        def decorated_view(*args, **kwargs):
#            if not current_user.is_authenticated:
#              return login_manager.unauthorized()
#            if ((current_user.is_admin != is_admin) and (is_admin != "ANY")):
#                return login_manager.unauthorized()
#            return fn(*args, **kwargs)
#        return decorated_view
#    return wrapper