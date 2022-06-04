<<<<<<< HEAD
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required, admin_required
import json
from app import admin, db, get_db_connection
from . import admin_bp
#from app.public import routes

@admin_bp.route('/crearEncuesta')
#@login_required
=======
from flask import render_template, url_for, request, jsonify,abort
from flask_login import current_user, login_required
from app.auth.routes import admin_required
import json
from collections import Counter
from app import admin, db
from . import admin_bp

@admin_bp.route('/crearEncuesta')
@login_required
@admin_required
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
def rutaCrearEncuesta():
    return render_template('admin/crearEncuesta.html')

@admin_bp.route('/guardarEncuesta', methods=['POST'] )
<<<<<<< HEAD
def guardar_encuesta():
    if request.method == 'POST':
        # try:
=======
@login_required
@admin_required
def guardar_encuesta():
    if request.method == 'POST':
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
        datosEncuesta = request.get_json(force = True)
        titulo=datosEncuesta[0]
        descripcion=datosEncuesta[1]
        fechaComienzo=datosEncuesta[2]
        fechaTermino=datosEncuesta[3]
        preguntas=datosEncuesta[4]
        numPreguntas=len(preguntas)

        try:
            sql = 'INSERT INTO encuesta (id_encuesta, titulo_encuesta, descripcion,fecha_comienzo,fecha_termino,preguntas[%s]) VALUES (DEFAULT,%s,%s,%s,%s,%s);'
            db.execute(sql, (numPreguntas,titulo,descripcion,fechaComienzo,fechaTermino,json.dumps(preguntas)))
<<<<<<< HEAD
        except Exception as e:
            print(e)

    return {"hola": "mundo!"}    

@admin_bp.route('/guardarEditEncuesta', methods=['POST'] )
=======
            return render_template('public/index.html')
        except Exception as e:
            print(e)

    return {"hola": "mundo!"}

@admin_bp.route('/guardarEditEncuesta', methods=['POST'] )
@login_required
@admin_required
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
def guardar_editar_encuesta():
    if request.method == 'POST':
        datosEncuesta = request.get_json(force = True)
        titulo=datosEncuesta[0]
        descripcion=datosEncuesta[1]
        fechaComienzo=datosEncuesta[2]
        fechaTermino=datosEncuesta[3]
        id=datosEncuesta[4]

        try: 
            sql = 'UPDATE encuesta SET titulo_encuesta = %s , descripcion = %s,fecha_comienzo = %s,fecha_termino = %s WHERE id_encuesta = %s'
            db.execute(sql, (titulo,descripcion,fechaComienzo,fechaTermino,id))
<<<<<<< HEAD
=======
            
            return render_template('admin/index.html')
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
        except Exception as e:
            print(e)

    return {"hola": "mundo!"}    

@admin_bp.route('/editarEncuesta/<string:id>/')
@login_required
@admin_required
def rutaEditarEncuesta(id):
    sentenciaSQL = '''\
    SELECT * FROM encuesta WHERE encuesta.id_encuesta = %s;'''
    db_data = db.fetch_all(sentenciaSQL,(str(id),))[0]

    if db_data is None:
        abort(404)

    return render_template('admin/editarEncuesta.html', db_data=db_data)

@admin_bp.route('/verEncuestas',methods=['GET', 'POST'])
@login_required
@admin_required
def rutaDesplegarEncuestas():
    db_data = None
    try:
        sentenciaSQL = '''\
<<<<<<< HEAD
        SELECT encuesta.id_encuesta,encuesta.titulo_encuesta FROM encuesta'''
=======
        SELECT encuesta.id_encuesta,encuesta.titulo_encuesta FROM encuesta ORDER BY encuesta.id_encuesta ASC'''
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
        db_data = db.fetch_all(sentenciaSQL,)
    except Exception as e:
            print(e)
    if db_data is None:
        abort(404)
    return render_template('admin/desplegarMisEncuestas.html', db_data=db_data)

<<<<<<< HEAD
@admin_bp.route('/verEncuestas')
def rutaDesplegarEncuestas():
    conn = get_db_connection()
    cur = conn.cursor()

    id_encuestas=db.fetch_all('SELECT id_encuesta from encuesta ORDER BY id_encuesta ASC;')
    #creo texto para usar en la sentencias sql seleccionando id de las encuestas con respecto al usuario
    text_id_encuesta = ''
    cantidad_id_encuesta = len(id_encuestas)

    for i in range(cantidad_id_encuesta):
        text_id_encuesta += 'id_encuesta = ' + str(id_encuestas[i][0])

        if i is not cantidad_id_encuesta - 1:
            text_id_encuesta += ' OR '
        else:
            text_id_encuesta += ' '
    
    #EXTRAE DATOS DE_TODO LO NECESARIO DE LA DB
    sentenciaSQL = '''\
    SELECT encuesta.id_encuesta, encuesta.titulo_encuesta, encuesta.descripcion, encuesta.fecha_comienzo, encuesta.fecha_termino,
    encuesta.preguntas FROM encuesta WHERE ''' + text_id_encuesta + '''ORDER BY encuesta.id_encuesta'''
    cur.execute(sentenciaSQL)
    db_data = cur.fetchall()
    cur.close()
    conn.close()

    id_encuesta = [item[0] for item in db_data]
    titulo_encuesta = [item[1] for item in db_data]
    descripcion_encuesta = [item[2] for item in db_data]
    fecha_comienzo_encuesta = [item[3] for item in db_data]
    fecha_termino_encuesta = [item[4] for item in db_data]
    preguntas_alternativas_encuesta = [item[5][0] for item in db_data]

    preguntas_encuesta = []
    alternativas_encuesta = []

    
    for i in range(len(preguntas_alternativas_encuesta)):
        preguntas = [item['Pregunta'] for item in preguntas_alternativas_encuesta[i]]
        alternativas = [item['Alternativas'] for item in preguntas_alternativas_encuesta[i]]
        
        preguntas_encuesta.append(preguntas)
        alternativas_encuesta.append(alternativas)
    
    datos = {"id":id_encuesta, "titulo":titulo_encuesta, "descripcion":descripcion_encuesta, "fecha_comienzo":fecha_comienzo_encuesta, 
            "fecha_termino":fecha_termino_encuesta, "preguntas":preguntas_encuesta, "alternativas":alternativas_encuesta}

    return render_template('admin/desplegarEncuestas.html', datos=datos)

@admin_bp.route('/get_word')
def get_prediction():
    id_encuesta = flask.request.args.get('id_encuesta')[0]
    conn = get_db_connection()
    cur = conn.cursor()

    sentenciaSQL = 'SELECT respuesta.respuestas FROM respuesta WHERE respuesta.id_encuesta = ' + id_encuesta + ';'
    cur.execute(sentenciaSQL)
    todas_respuestas = cur.fetchall()
    if(len(todas_respuestas) == 0):
        return flask.jsonify({'porcentajes':'No hay respuestas'})

=======
@admin_bp.route("/verEncuestas/<string:id>/")
@login_required
@admin_required
def mostrar_preguntas_alternativas(id):
    sentenciaSQL = '''\
    SELECT * FROM encuesta WHERE encuesta.id_encuesta = %s;'''
    db_data = db.fetch_all(sentenciaSQL,(str(id),))[0]

    if db_data is None:
        abort(404)
    return render_template('admin/desplegarVerEncuesta.html',db_data=db_data)

@admin_bp.route('/obtener_respuestas')
@login_required
@admin_required
def obtener_respuestas():
    print("estoy obteniendo las respuestas")
    id_encuesta = request.args.get('id_encuesta')[0]

    sentenciaSQL = 'SELECT respuesta.respuestas FROM respuesta WHERE respuesta.id_encuesta = %s;'
    todas_respuestas = db.fetch_all(sentenciaSQL,str(id_encuesta))

    if(len(todas_respuestas) == 0):
        return jsonify({'porcentajes':'No hay respuestas'})

    print("todas las respuestas:",todas_respuestas) #POSIBLE OPTIMIZACION
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
    #respuestas = [item[4]['Respuestas'] for item in todas_respuestas]
    respuestas = [item[0]['Respuestas'] for item in todas_respuestas]
    n_preguntas = len(respuestas[0])
    porcentajes = []
    
    for i in range(n_preguntas):
        porcentajes_i = []
        respuesta_i = [x[i] for x in respuestas]
        count = Counter(respuesta_i)
        total = sum(count.values())
        for i in range(len(respuestas)):
            porcentajes_i.append(count[str(i+1)] / total * 100)
        porcentajes.append(porcentajes_i)
<<<<<<< HEAD
    return flask.jsonify({'porcentajes':porcentajes})
    
@admin_bp.route('/agregarmail')
def agregarmail():
    return render_template('admin/agregarmails.html')
=======
    return jsonify({'porcentajes':porcentajes})
    
@admin_bp.route('/agregarmails')
@login_required
@admin_required
def agregarmail():
    return render_template('admin/agregarmails.html')

@admin_bp.route('/insertarmail',methods=['POST'])
@login_required
@admin_required
def insertarmail():
    if request.method == 'POST':
        correo = request.form['mail']
        conn = get_db_connection()
        suscrito= True
        cur = conn.cursor()
        cur.execute('INSERT INTO mails values(%s,%s)',(correo,suscrito))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('agregarmail'))
>>>>>>> f887af468785d130194acbcb78a3d9d1bf04ca04
