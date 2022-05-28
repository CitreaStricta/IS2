from flask import render_template,redirect,url_for, request
from werkzeug.urls import url_parse
from forms import LoginForm
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from __init__ import app

from base_de_datos_prueba import users,get_user
from usuario import User

login_manager = LoginManager(app)
#login_manager.login_view = "login"

@login_manager.user_loader
def load_user(email):
    return User.get_by_email(email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('rutaBase'))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        passoword = form.password.data
        remember = form.remember_me.data

        user = User.select_user(email)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('rutaBase')
            return redirect(next_page)
        else:
            error = f'Datos incorrectos, intentelo nuevamente'
    return render_template('login_form.html', form=form,error=error)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('rutaBase'))