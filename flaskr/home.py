from flask import render_template
from __init__2 import app

@app.route('/')
def rutaBase():
    return render_template('home.html')