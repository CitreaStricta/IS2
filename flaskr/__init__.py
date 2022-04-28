import os

from flask import Flask, render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import jyserver.Flask as jsf

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
        #COMPROBAR QUE LOS DATOS ESTEN BIEN POR LA BASE DE DATOS
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

    @app.route('/encuestas_privadas',methods=["POST","GET"])
    def rutaEncuestas_privadas():
        #SELECCIONAR LAS ENCUESTAS DEL USUARIO LOGGEADO
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
        nombre_encuestas = ['Encuesta 1','Encuesta 2']
        preguntas = []
        respuestas = []
        for i in range(len(nombre_encuestas)):
            numero_de_preguntas = 2
            preg_por_enc = []
            resp_por_enc = []
            for j in range(numero_de_preguntas):
                resp_por_preg = []
                preg_por_enc.append('Hola/encuesta '+str(i))
                numero_de_respuestas = 2
                for k in range(numero_de_respuestas):
                    resp_por_preg.append('Adios/encuesta '+str(i))
                resp_por_enc.append(resp_por_preg)
            preguntas.append(preg_por_enc)
            respuestas.append(resp_por_enc)
        encuesta_activa = -1
        data = {'nombre_encuestas':nombre_encuestas,'preguntas':preguntas,'respuestas':respuestas,'encuesta_activa':encuesta_activa}
        if request.method == "POST":
            encuesta_seleccionada = list(request.form.keys())[0]
            print(encuesta_seleccionada)
            data['encuesta_activa'] = int(encuesta_seleccionada)
            return render_template('encuestas_privadas.html',data = data)
        else:
            return render_template('encuestas_privadas.html',data = data)
        return render_template('encuestas_privadas.html',data = data)

    @app.route('/preguntas_privadas')    
    def rutaPreguntas_privadas():
        name = "hola"
        if request.method == 'POST':
            return render_template('home.html',name)
        else:
            return render_template('home.html',name)
        name = "hola"
        return render_template('home.html',name)



    @app.route('/linkEncuesta/parametros de info para reconocer en BD o algo similar')
    def encuesta():
        return render_template('lugarDondeSeAlmacenaLaEncuesta.html')

    return app
    
    #@jsf.use(app)
    #class App:
    #    def __init__(self):

'''
@app.route('/antenas', methods=['GET'])
def antenas():
    return render_template('antenas.html') #el sistema sabe que tiene que buscar en la carpeta templates, por lo que

'''