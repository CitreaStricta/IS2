from ensurepip import bootstrap
from flask import Flask,render_template
from flask_login import LoginManager
from .database import Database ,get_db_connection

login_manager = LoginManager()

db = Database(
    db = "d28t56b7dpk32k",
    user = "zntctcuflomgsk",
    password = "43061258b91aaa3cf85b9c222443c57f889531d4478e8e0e69abcd715daf419c",
    port = "5432",
    host = "ec2-52-5-110-35.compute-1.amazonaws.com"
)

def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404

    @app.errorhandler(401)
    def error_404_handler(e):
        return render_template('401.html'), 401

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

    #Manejador de Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    #Errores
    register_error_handlers(app)
    


    return app