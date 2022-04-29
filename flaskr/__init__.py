import os
import psycopg2
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

def get_db_connection():
    DBHOST="ec2-52-5-110-35.compute-1.amazonaws.com"
    DATABASE="d28t56b7dpk32k"
    DBUSER="zntctcuflomgsk"
    DBPASSWORD="43061258b91aaa3cf85b9c222443c57f889531d4478e8e0e69abcd715daf419c"
    DBPORT= "5432"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (DBHOST, DBPORT, DBUSER, DBPASSWORD, DATABASE)
    conn = psycopg2.connect(connstr)
    return conn


def create_app(test_config=None):
    # create and configure the app
    # Flask() crea la instancia de Flask
    # __name__ define el nombre del modulo de python, para conocer donde buscarlos
    # instace_relative_config=true indica que los files de configuración se encuentran
    #   en el folder  de esta instancia
    app = Flask(__name__, instance_relative_config=True)
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

    # @app.route() crea una ruta y retorna lo que se despliegara en dicha ruta.
    @app.route('/')
    def rutaBase():
        return render_template('home.html')
        
    @app.route('/login')
    def rutaLogin():
        return render_template('login.html')

    @app.route('/prueba')
    def rutaPrueba():
        return render_template('prueba.html')

    @app.route('/logged')
    def rutaLogged():
        '''
        import pymysql 
        import sys
        host='localhost'
        user = 'root'
        password = ''
        db = 'skripsi'

        try:
            con = pymysql.connect(host=host,user=user,password=password,db=db, use_unicode=True, charset='utf8')
            print('+=========================+')
            print('|  CONNECTED TO DATABASE  |')
            print('+=========================+')
        except Exception as e:
            sys.exit('error',e)
        cur = con.cursor()
        #cur.execute("SELECT * FROM dataset") #QUERY
        data = cur.fetchall()
        '''
        user_details = {'name': 'John', 'password': 'hola123'}
        return render_template('logged.html', user=user_details)

    @app.route('/encuestas_privadas')
    def rutaEncuestas_privadas():
        return render_template('encuestas_privadas.html')

    @app.route('/linkEncuesta/parametros de info para reconocer en BD o algo similar')
    def encuesta():
        return render_template('lugarDondeSeAlmacenaLaEncuesta.html')

    @app.route('/bd')
    def index():
        conn = get_db_connection()
        cur = conn.cursor()
        sentenciaSQL = 'SELECT * FROM encuestado;'
        cur.execute(sentenciaSQL)
        bdEncuestados = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('pruebaBD.html', encuestados=bdEncuestados)

    return app


'''
@app.route('/antenas', methods=['GET'])
def antenas():
    return render_template('antenas.html') #el sistema sabe que tiene que buscar en la carpeta templates, por lo que

'''