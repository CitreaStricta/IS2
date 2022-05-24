from flask import render_template
from __init__ import app

@app.route('/')
def rutaBase():
    return render_template('home.html')