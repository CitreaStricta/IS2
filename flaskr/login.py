from flask import render_template
from __init__ import app

@app.route('/login')
def rutaLogin():
    return render_template('login.html')