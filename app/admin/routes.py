from flask import render_template, url_for, request, jsonify
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

@admin_bp.route('/editarEncuesta', methods=['GET', 'POST'])
@login_required
@admin_required
def rutaEditarEncuesta():
    idEncuesta = request.form.get("encuestaSeleccionada")
    
    #EXTRAE DATOS DE_TODO LO NECESARIO DE LA DB
    sentenciaSQL = '''\
    SELECT encuesta.id_encuesta, encuesta.titulo_encuesta, encuesta.descripcion, encuesta.fecha_comienzo, encuesta.fecha_termino,
    encuesta.preguntas FROM encuesta WHERE id_encuesta = %s;'''
    db_data = db.fetch_all(sentenciaSQL,str(idEncuesta))

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

    return render_template('admin/editarEncuesta.html', datos=datos)

@admin_bp.route('/verEditarEncuestas')
@login_required
@admin_required
def rutaEditarEncuestas():
    # EN VOLA ESTO DSPS HAY QUE EDITARLO 
    id_encuestas = [1,2,3,4,5,6,7,8,9,10] #encuestas a seleccionar

    try:
        strings = '%s,'*(len(id_encuestas)-1) + '%s'
        sentenciaSQL = '''\
        SELECT encuesta.id_encuesta, encuesta.titulo_encuesta, encuesta.descripcion, encuesta.fecha_comienzo, encuesta.fecha_termino,
        encuesta.preguntas FROM encuesta WHERE id_encuesta in ('''+ strings +''') ORDER BY encuesta.id_encuesta'''
        db_data = db.fetch_all(sentenciaSQL,tuple(id_encuestas))
    except Exception as e:
            print(e)

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

    return render_template('admin/desplegarEditarEncuestas.html', datos=datos)

@admin_bp.route('/verEncuestas')
@login_required
@admin_required
def rutaDesplegarEncuestas():

    id_encuestas = [1,2,3,4,5,6,7,8] #encuestas a seleccionar

    try:
        strings = '%s,'*(len(id_encuestas)-1) + '%s'
        sentenciaSQL = '''\
        SELECT encuesta.id_encuesta, encuesta.titulo_encuesta, encuesta.descripcion, encuesta.fecha_comienzo, encuesta.fecha_termino,
        encuesta.preguntas FROM encuesta WHERE id_encuesta in ('''+ strings +''') ORDER BY encuesta.id_encuesta'''
        db_data = db.fetch_all(sentenciaSQL,id_encuestas)
    except Exception as e:
            print(e)
    print(db_data)
    '''
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

    return render_template('admin/desplegarEncuestas copy.html', datos=datos)
    '''
    return render_template('admin/desplegarEncuestas.html', db_data=db_data)

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
    
@admin_bp.route('/agregarmail')
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