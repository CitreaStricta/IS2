import os
from flask import Flask,request,url_for #necesario
from flask_sqlalchemy import SQLAlchemy
import json
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap #obligatorio
from flask_wtf import FlaskForm

class SurveyForm(FlaskForm):
    pass

def create_app(test_config=None):
    # create and configure the app
    # Flask() crea la instancia de Flask
    # __name__ define el nombre del modulo de python, para conocer donde buscarlos
    # instace_relative_config=true indica que los files de configuración se encuentran
    #   en el folder  de esta instancia
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)
    # indicar algunas configuraciones POR DEFECTO de la app (sin config.py)
    app.config.from_mapping(
        SECRET_KEY='dev', # usada para mantener los datos seguros
        # path donde se almacenara la info de SQLite, revisar para otros
        #   gestores de BD
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None: # si existe config.py
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else: # Si existe test.config se usaran estas para probar el codigo
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try: # se asegura que exista carpeta de app.instance_path para almacenar datos
         #   de la BD
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app

app = create_app()

from home import *
from login import *
from encuesta import *



if __name__ == '__main__':
    app.run(port = 5000, debug = True)
