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
def rutaCrearEncuesta():
    return render_template('admin/crearEncuesta.html')

@admin_bp.route('/guardarEncuesta', methods=['POST'] )
@login_required
@admin_required
def guardar_encuesta():
    if request.method == 'POST':
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
            return render_template('public/index.html')
        except Exception as e:
            print(e)

    return {"hola": "mundo!"}

@admin_bp.route('/guardarEditEncuesta', methods=['POST'] )
@login_required
@admin_required
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
            
            return render_template('admin/index.html')
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
        SELECT encuesta.id_encuesta,encuesta.titulo_encuesta FROM encuesta'''
        db_data = db.fetch_all(sentenciaSQL,)
    except Exception as e:
            print(e)
    if db_data is None:
        abort(404)
    return render_template('admin/desplegarMisEncuestas.html', db_data=db_data)

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