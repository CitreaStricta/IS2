import os
import psycopg2
from flask import Flask, render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
import json
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from collections import Counter

class SurveyForm(FlaskForm):
    pass

def get_db_connection():
    #xd xdxdfxdxdxdxd xdididi
    DBHOST="ec2-52-5-110-35.compute-1.amazonaws.com"
    DATABASE="d28t56b7dpk32k"
    DBUSER="zntctcuflomgsk"
    DBPASSWORD="43061258b91aaa3cf85b9c222443c57f889531d4478e8e0e69abcd715daf419c"
    DBPORT= "5432"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (DBHOST, DBPORT, DBUSER, DBPASSWORD, DATABASE)
    conn = psycopg2.connect(connstr)
    return conn


# hay que cambiar esta funcion para que no tenga las rutas dentro de ella (separar las funciones internas de 'rutas' de la funcion que crea la app 'create app')
def create_app(test_config=None):
    # create and configure the app
    # Flask() crea la instancia de Flask
    # __name__ define el nombre del modulo de python, para conocer donde buscarlos
    # instace_relative_config=true indica que los files de configuración se encuentran
    #   en el folder  de esta instancia
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)
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

    @app.route('/crearEncuesta')
    def rutaCrearEncuesta():
        return render_template('crearEncuesta.html')

    @app.route('/guardarEncuesta', methods=['POST'] ) # esto va
    def guardar_encuesta():
        if request.method == 'POST':
            # try:
            preguntas = []
            list_of_json = request.get_json(force=True)
            for i in range(len(list_of_json)-1):
            # print(list_of_json[i]['questionText'])
            # preguntas = preguntas + [[list_of_json[i]['typeValue'], list_of_json[i]['questionText']]]
                preguntas.append([list_of_json[i]['typeValue'], list_of_json[i]['questionText']])
            # except Exception as e:
            # print(e)
            # parcear las preguntas para entregarselas a la base de datos
            dict_a = {"Preguntas": preguntas}
            print(dict_a)

            try:
                conn = get_db_connection()
                cur = conn.cursor()
                print(list_of_json[len(list_of_json)-1])
                #insert into encuesta values (1,'Como te sientes', '{"Preguntas": [["texto","¿Como te sientes hoy?"],["texto","¿Como te sentiste ayer?"]]}')
                sql = 'INSERT INTO encuesta (id_encuesta, titulo_encuesta, preguntas) VALUES (DEFAULT,%s,%s);'
                cur.execute(sql, (list_of_json[len(list_of_json)-1],json.dumps(dict_a)))
                # print(cur.fetchone()[0])
                # cur.execute('INSERT INTO encuesta[p')
                    # sql = 'INSERT INTO pregunta(id_pregunta, tipo, encabezado, encuesta_asociada)'
                    # cur.execute(sql, list_of_json[i]['questionNumber'], list_of_json[i]['typeValue'], list_of_json[i]['questionText'], list_of_json[i]['questionText'])
                    # cur.execute('SELECT * FROM encuestado;')
                    # id = cur.fetchone()[0]
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(e)

        return {"hola": "mundo!"}

    '''
    @app.route('/guardarRespuesta', methods=['POST'] ) # Agregar parametro en el link
    def guardar_encuesta():
        if request.method == 'POST':
            # try:
            preguntas = []
            list_of_json = request.get_json(force=True)
            for i in range(len(list_of_json)):
            # print(list_of_json[i]['questionText'])
            # preguntas = preguntas + [[list_of_json[i]['typeValue'], list_of_json[i]['questionText']]]
                preguntas.append([list_of_json[i]['typeValue'], list_of_json[i]['questionText']])
            # except Exception as e:
            # print(e)
            # parcear las preguntas para entregarselas a la base de datos
            dict_a = {"Preguntas": preguntas}
            print(dict_a)

            # print(json.dumps(json_preguntas))
            print(json_preguntas)
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                #insert into encuesta values (1,'Como te sientes', '{"Preguntas": [["texto","¿Como te sientes hoy?"],["texto","¿Como te sentiste ayer?"]]}')
                sql = 'INSERT INTO responde (id_encuesta, titulo_encuesta, preguntas) VALUES (%s,%s,%s);'
                cur.execute(sql, ('4', 'primera encuesta de prueba',json.dumps(dict_a)))
                # print(cur.fetchone()[0])
                # cur.execute('INSERT INTO encuesta[p')
                    # sql = 'INSERT INTO pregunta(id_pregunta, tipo, encabezado, encuesta_asociada)'
                    # cur.execute(sql, list_of_json[i]['questionNumber'], list_of_json[i]['typeValue'], list_of_json[i]['questionText'], list_of_json[i]['questionText'])
                    # cur.execute('SELECT * FROM encuestado;')
                    # id = cur.fetchone()[0]
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(e)

        return {"hola": "mundo!"}
    '''

    @app.route('/mostrarEncuesta')
    def show_survey():
        conn = get_db_connection()
        cur = conn.cursor()
        sentenciaSQL = 'SELECT * FROM encuesta WHERE id_encuesta = 1;'
        cur.execute(sentenciaSQL)
        bdPreguntas = cur.fetchall()
        cur.close()
        conn.close()
        print(bdPreguntas)
        titulo = []
        preguntas= []
        tipo_preguntas = []
        # la forma que viene es (0: identificador, 1: Titulo y 2: preguntas)
        for i in range(len(bdPreguntas)):
            preguntas_encuesta_i = []
            tipo_encuesta_i = []
            titulo.append(bdPreguntas[i][1])

            for pregunta in bdPreguntas[i][2]['Preguntas']:
                print("tipo pregunta:",pregunta[0])
                print("nombre pregunta:",pregunta[1])

                tipo_encuesta_i.append(pregunta[0])
                preguntas_encuesta_i.append(pregunta[1])

            preguntas.append(preguntas_encuesta_i)
            tipo_preguntas.append(tipo_encuesta_i)


        data = {"Encuestas":titulo,"Preguntas":preguntas,"Tipo":tipo_preguntas}
        return render_template('mostrarEncuesta.html', encuestas=data)
        '''
        class DynamicForm(SurveyForm):
            pass

        connection = get_db_connection()
        cursor = connection.cursor()
        sentenciaSQL = 'SELECT * FROM encuesta WHERE id_encuesta = 1;' #cambiar forma dinamica de id
        cursor.execute(sentenciaSQL)
        result = cursor.fetchone()
        
        
        if result is not None:
            title = result[1] #titulo de la encuesta
            dict_of_questions = result[2] #Diccionario con preguntas

            list_of_questions = dict_of_questions["Preguntas"]

            for index, list_of_question in enumerate(list_of_questions):
                question = list_of_question[1]
                setattr(DynamicForm, "questionNumber"+str(index) ,StringField(question, validators=[DataRequired()]) )
            setattr(DynamicForm, "submitQuestion", SubmitField("Enviar"))

            form = DynamicForm()
        
            if form.validate_on_submit():
                print("Enviado")
                return render_template("mostrarEncuesta.html", form=form , title=title)
        return render_template("mostrarEncuesta.html", form=form, title=title)
        '''
    
    @app.route('/verEncuestas')
    def rutaDesplegarEncuestas():
        conn = get_db_connection()
        cur = conn.cursor()

        id_encuestas = [1,2,3] #encuestas a seleccionar

        #creo texto para usar en la sentencias sql seleccionando id de las encuestas con respecto al usuario
        text_id_encuesta = ''
        cantidad_id_encuesta = len(id_encuestas)

        for i in range(cantidad_id_encuesta):
            text_id_encuesta += 'id_encuesta = ' + str(id_encuestas[i])

            if i is not cantidad_id_encuesta - 1:
                text_id_encuesta += ' OR '
            else:
                text_id_encuesta += ';'

        #EXTRAE DATOS DE_TODO LO NECESARIO DE LA DB
        sentenciaSQL = '''\
        SELECT encuesta.id_encuesta, encuesta.titulo_encuesta, encuesta.descripcion, encuesta.fecha_comienzo, encuesta.fecha_termino,
        encuesta.preguntas, json_agg(respuesta.respuestas) FROM encuesta Full Outer Join respuesta On encuesta.id_encuesta = respuesta.id_encuesta 
        GROUP BY encuesta.id_encuesta ORDER BY encuesta.id_encuesta'''
        cur.execute(sentenciaSQL)
        db_data = cur.fetchall()
        cur.close()
        conn.close()

        #Obtenemos los datos en forma mas ordeanda
        
        id_p = []
        titulo = []
        preguntas= []
        alternativas = []
        respuestas = []
        
        for i in range(len(db_data)):
            #db_data = (id_encuesta , titulo , descrip , t_inicio , t_final , [[Pregunta:{},Alternativas:{}]] , respuesta_1 , ... , respuesta_n)
            #respuesta_i es un json, para obtener datos usar ['Respuestas']
            preguntas_encuesta_i = []
            alternativas_encuesta_i = []

            id_p.append(db_data[i][0])
            titulo.append(db_data[i][1])

            for pregunta_alternativa in db_data[i][5][0]:

                preguntas_encuesta_i.append(pregunta_alternativa['Pregunta'])

                alternativas_encuesta_i.append(pregunta_alternativa['Alternativas'])

            preguntas.append(preguntas_encuesta_i)

            alternativas.append(alternativas_encuesta_i)

            respuestas.append(db_data[i][6])
        
        print(preguntas)

        #Agrupar respuestas

        respuestas_procesadas = []
        for i , respuestas_encuesta_i in enumerate(respuestas):
            #encuesta_i

            respuestas_proc_pregunta =  [[] for i in range(len(preguntas[i]))]

            for j, respuestas_pregunta_j in enumerate(respuestas_encuesta_i):
                #pregunta i

                if respuestas_pregunta_j is None:
                    continue

                for k, r_i in enumerate(respuestas_pregunta_j['Respuestas']):
                    respuestas_proc_pregunta[k].append(r_i)

            respuestas_procesadas.append(respuestas_proc_pregunta)

        #Procesar respuestas
        
        #resultados = []
        porcentajes = []
        for i, respuesta_encuesta_i in enumerate(respuestas_procesadas):

            #resultados_encuesta_i = []
            porcentajes_encuesta_i = []

            for j, respuesta_pregunta_j in enumerate(respuesta_encuesta_i):

                result_pregunta = dict(Counter(respuesta_pregunta_j))
                lista_keys = list(result_pregunta.keys())
                n_preguntas = len(list(result_pregunta.keys()))

                guarda_respuestas = [[] for i in range(n_preguntas+1)]

                if result_pregunta == {}: 
                    guarda_respuestas[0] = "No hay respuestas"
                    porcentajes_encuesta_i.append(guarda_respuestas)
                    continue

                for n in range(n_preguntas):

                    guarda_respuestas[int(lista_keys[n])] = int(result_pregunta[lista_keys[n]])/ len(respuesta_pregunta_j) * 100

                porcentajes_encuesta_i.append(guarda_respuestas)
            porcentajes.append(porcentajes_encuesta_i)
        print("porcentajes",porcentajes)
        print(porcentajes[0][0][0])
        print(porcentajes[0][0][1])


        data = {"Id":id_p, "Encuestas":titulo, "Preguntas":preguntas, "Alternativas":alternativas, "Porcentajes":porcentajes}
        #print("data",data)
        return render_template('desplegarEncuestas.html', encuestas=data)
        
    @app.route('/login')
    def rutaLogin():
        return render_template('login.html')

    @app.route('/logged')
    def rutaLogged():
        return render_template('logged.html')
        

    @app.route('/encuestas_privadas',methods=["POST","GET"])
    def rutaEncuestas_privadas():
        id_encuestador = 0
        conn = get_db_connection()
        cur = conn.cursor()

        sentenciaSQL = 'SELECT * FROM encuesta,encuestador WHERE encuestador.id_encuestador =' + str(id_encuestador) + ';'
        cur.execute(sentenciaSQL)
        sa = cur.fetchall()

        sentenciaSQL = 'SELECT * FROM encuestado;'
        cur.execute(sentenciaSQL)
        bdEncuestados = cur.fetchall()

        sentenciaSQL = 'SELECT * FROM encuestador;'
        cur.execute(sentenciaSQL)
        bdEncuestador = cur.fetchall()

        cur.close()
        conn.close()
        print(bdEncuestados)
        print(bdEncuestador)
        print(sa)




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
            print("entre")
            encuesta_seleccionada = list(request.form.keys())[0]
            print(encuesta_seleccionada)
            data['encuesta_activa'] = int(encuesta_seleccionada)
            return render_template('encuestas_privadas.html',data = data)
        else:
            return render_template('encuestas_privadas.html',data = data)
        return render_template('encuestas_privadas.html',data = data)

        #return render_template('logged.html', encuestados=bdEncuestados)
        #return render_template('encuestas_privadas.html')

    @app.route('/linkEncuesta/parametros de info para reconocer en BD o algo similar')
    def encuesta():
        return render_template('lugarDondeSeAlmacenaLaEncuesta.html')

    @app.route('/verResumenEncuestas')
    def verResumenEncuesta():
        conn = get_db_connection()
        cur = conn.cursor()

        id_encuestas = [1,2,3] #encuestas a seleccionar

        text_id_encuesta = ''
        cantidad_id_encuesta = len(id_encuestas)

        for i in range(cantidad_id_encuesta):
            text_id_encuesta += 'id_encuesta = ' + str(id_encuestas[i])

            if i is not cantidad_id_encuesta - 1:
                text_id_encuesta += ' OR '
            else:
                text_id_encuesta += ';'
        
        #EXTRAE DATOS DE LAS ENCUESTAS EN LA DB
        sentenciaSQL = 'SELECT * FROM encuesta WHERE ' + text_id_encuesta
        print("Sentencia SQL",sentenciaSQL)
        cur.execute(sentenciaSQL)
        bdEncuestas = cur.fetchall()
        
        #EXTRAE DATOS DE LAS RESPUESTAS DE LA DB
        sentenciaSQL = 'SELECT * FROM respuesta WHERE ' + text_id_encuesta
        cur.execute(sentenciaSQL)
        bdRespuestas = cur.fetchall()

        cur.close()
        conn.close()


        print("*"*60)
        print("bd_encuestas",bdEncuestas)
        print("bd_respuestas",bdRespuestas)
        return render_template('verResumenEncuestas.html',data = bdRespuestas)

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
