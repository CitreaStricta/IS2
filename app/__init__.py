import logging
from flask import Flask,render_template
from flask_login import LoginManager
from logging.handlers import SMTPHandler
from flask_mail import Mail
from .database import Database ,get_db_connection
from flask_bootstrap import Bootstrap
from .tasks.scheduler import scheduler

login_manager = LoginManager()
mail = Mail()

db = Database(
    db = "d28t56b7dpk32k",
    user = "zntctcuflomgsk",
    password = "43061258b91aaa3cf85b9c222443c57f889531d4478e8e0e69abcd715daf419c",
    port = "5432",
    host = "ec2-52-5-110-35.compute-1.amazonaws.com"
)


def configure_mail(app):
    mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                app.config['DONT_REPLY_FROM_EMAIL'],
                                app.config['ADMINS'],
                                '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
                                (app.config['MAIL_USERNAME'],
                                app.config['MAIL_PASSWORD']),
                                ())
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(mail_handler_formatter())
    app.logger.addHandler(mail_handler)


def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d
            Message:
            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
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
    app.config['APP_ENV'] = 'development'
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587   
    app.config['MAIL_USERNAME'] = 'mails.empresa.is@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wctlzgvdtukryohr'
    app.config['ADMINS'] = ('mails.empresa.is@gmail.com', )
    app.config['DONT_REPLY_FROM_EMAIL'] = 'mails.empresa.is@gmail.com'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    configure_mail(app)
    #Manejador de Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    mail.init_app(app)
    scheduler.init_app(app)
    with app.app_context():
        from .tasks import task
        scheduler.start()

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .surveys import surveys_bp
    app.register_blueprint(surveys_bp)
    
    #bootstrap
    Bootstrap(app)

    #Errores
    register_error_handlers(app)
    
    return app