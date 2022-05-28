from flask import Flask
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
db.connect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    #from .admin import admin_bp
    #app.register_blueprint(admin_bp)
    from .public import public_bp
    app.register_blueprint(public_bp)
    return app