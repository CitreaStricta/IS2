from flask import render_template
from __init__2 import app

@app.route('/login')
def rutaLogin():
    return render_template('login.html')