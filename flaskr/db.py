# Establece la base de datos que va a ser utilizada, en este caso sqlite.
# Podria ser SQL_Alchemy

import sqlite3

import click
# 'g' es un objeto unico para cada request. Es utilizado para almacenar 
# datos que podran ser accedidos por multiples request de funciones.
# La conexión es reutilizada en vez de abrir una nueva cuando se usa 
# 'get_db'
# 'current_app' objeto especial que apunta a la app para manejar la request 
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # sqlite3.connect() establece una conexión con el archivo apuntado
        # por la DATABASE configuration key
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# Revisa si existe una conexión, en caso de que exista la cierra.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()