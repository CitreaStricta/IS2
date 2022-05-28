from flask import render_template, request, redirect, url_for
from forms import SignupForm
from __init__ import app
from flask_login import current_user,login_user
from base_de_datos_prueba import users,get_user
from usuario import User

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('rutaBase'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.select_user(email)
        #user = None

        #print(user)
        if user is None:
            # Creamos el usuario y lo guardamos
            user = User(name,email, password)
            print(name,email,password)
            user.set_password(password)
            user.insert_user()
            #Lo dejamos logeado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('rutaBase')
            return redirect(next_page)
        else: 
            error = f'El email {email} ya está siendo utilizado por otro usuario'
    return render_template("signup_form.html", form=form,error=error)