from flask import render_template, url_for, request, jsonify,abort,current_app
from sqlalchemy import true
from flask_login import current_user, login_required
from app.auth.routes import admin_required
from collections import Counter
from app import admin, db
from . import admin_bp
from .forms import MailForm
import re
import json

@admin_bp.route('/crearEncuesta')
@login_required
@admin_required
def rutaCrearEncuesta():
    return render_template('admin/crearEncuesta.html')

@admin_bp.route('/guardarEncuesta', methods=['POST'] )
@login_required
@admin_required
def guardar_encuesta():
    print("guardar encuesta")
    if request.method == 'POST':
        datosEncuesta = request.get_json(force = True)
        titulo = datosEncuesta[0]
        descripcion = datosEncuesta[1]
        fechaComienzo = datosEncuesta[2]
        fechaTermino = datosEncuesta[3]
        preguntas = datosEncuesta[4]
        numPreguntas = len(preguntas)

        print(datosEncuesta)

        try:
            sql = 'INSERT INTO encuesta (id_encuesta, titulo_encuesta, descripcion,fecha_comienzo,fecha_termino,preguntas[%s]) VALUES (DEFAULT,%s,%s,%s,%s,%s);'
            db.connect()
            db.execute(sql, (numPreguntas,titulo,descripcion,fechaComienzo,fechaTermino,json.dumps(preguntas)))
            print("Se guarda encuesta correctamente")
            return {"status": "success"}
        except Exception as e:
            print(e)
            return {"status":"error"}
    return {"status": "success"}

@admin_bp.route('/guardarEditEncuesta', methods=['POST'] )
@login_required
@admin_required
def guardar_editar_encuesta():
    if request.method == 'POST':
        datosEncuesta = request.get_json(force = True)
        titulo = datosEncuesta[0]
        descripcion = datosEncuesta[1]
        fechaComienzo = datosEncuesta[2]
        fechaTermino = datosEncuesta[3]
        id = datosEncuesta[4]

        try: 
            sql = 'UPDATE encuesta SET titulo_encuesta = %s , descripcion = %s,fecha_comienzo = %s,fecha_termino = %s WHERE id_encuesta = %s'
            db.connect()
            db.execute(sql, (titulo,descripcion,fechaComienzo,fechaTermino,id))
            db.close()
            return {"hola": "mundo!"}
        except Exception as e:
            print(e)

    return {"hola": "mundo!"}    

@admin_bp.route('/editarEncuesta/<string:id>/')
@login_required
@admin_required
def rutaEditarEncuesta(id):
    sentenciaSQL = '''\
    SELECT * FROM encuesta WHERE encuesta.id_encuesta = %s;'''
    db.connect()
    db_data = db.fetch_all(sentenciaSQL,(str(id),))[0]
    db.close()

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
        SELECT encuesta.id_encuesta,encuesta.titulo_encuesta FROM encuesta ORDER BY encuesta.id_encuesta ASC'''
        db.connect()
        db_data = db.fetch_all(sentenciaSQL,)
        db.close()
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
    db.connect()
    db_data = db.fetch_all(sentenciaSQL,(str(id),))[0]
    db.close()

    if db_data is None:
        abort(404)
    return render_template('admin/desplegarVerEncuesta.html',db_data=db_data)

@admin_bp.route('/obtener_respuestas')
@login_required
@admin_required
def obtener_respuestas():
    print("estoy obteniendo las respuestas")
    id_encuesta = request.args.get('id_encuesta')
    print(id_encuesta)

    db.connect()
    sentenciaSQL = 'SELECT respuesta.respuestas FROM respuesta WHERE respuesta.id_encuesta = %s;'
    todas_respuestas = db.fetch_all(sentenciaSQL,(str(id_encuesta),))

    sentenciaSQL = 'SELECT encuesta.preguntas FROM encuesta WHERE encuesta.id_encuesta = %s;'
    todas_preguntas = db.fetch_one(sentenciaSQL,(str(id_encuesta),))
    db.close()

    if(len(todas_respuestas) == 0):
        return jsonify({'porcentajes':'No hay respuestas'})

    #print("todas las respuestas:",todas_respuestas) #POSIBLE OPTIMIZACION
    #print("todas las preguntas",todas_preguntas[0][0][0])
    #respuestas = [item[4]['Respuestas'] for item in todas_respuestas]
    respuestas = [item[0]['Respuestas'] for item in todas_respuestas]
    n_preguntas = len(respuestas[0])
    porcentajes = []
    numero_de_respuestas = []
    
    for i in range(n_preguntas):
        numero_de_respuestas_i = []
        porcentajes_i = []
        respuesta_i = [x[i] for x in respuestas]
        count = Counter(respuesta_i)
        total = sum(count.values())
        for i in range(len(todas_preguntas[0][0][i]['Alternativas'])):
            numero_de_respuestas_i.append(count[str(i+1)])
            #print("counter",count[str(i+1)])
            porcentajes_i.append(count[str(i+1)] / total * 100)
        
        numero_de_respuestas.append(numero_de_respuestas_i)
        porcentajes.append(porcentajes_i)
    #print(porcentajes)
    
    return jsonify({'porcentajes':porcentajes, 'n_respuestas':numero_de_respuestas}) #devuelve el porcentaje

@admin_bp.route('/agregarmails',methods=['GET','POST'])
@login_required
@admin_required
def insertarmail():
    form = MailForm()
    error = None
    creado = None
    if request.method == 'POST':
        if form.validate_on_submit():
            email=form.email.data
            if form.submit.data:
                db.connect()
                correos=db.fetch_all('SELECT * FROM mails ORDER BY correo ASC')
                correo=db.fetch_one('SELECT * FROM mails where correo=%s',(email,))
                db.close()
                if correo != None:
                    if correo[1] == True:
                        error= f'Mail ya existente en la base de datos'
                        return render_template('admin/agregarmails.html',form=form,error=error,db_data=correos)
                    else:
                        suscrito= True
                        db.connect()
                        db.execute('UPDATE mails SET suscrito=%s where correo=%s',(suscrito,correo[0]))
                        creado= f'Mail resuscrito exitosamente'
                        correos=db.fetch_all('SELECT * FROM mails ORDER BY correo ASC')
                        db.close()
                        return render_template('admin/agregarmails.html', form=form,creado=creado,db_data=correos)
                suscrito= True
                db.connect()
                db.execute('INSERT INTO mails values(%s,%s)',(email,suscrito))
                creado= f'Mail ingresado exitosamente'
                correos=db.fetch_all('SELECT * FROM mails ORDER BY correo ASC')
                db.close()
                return render_template('admin/agregarmails.html', form=form,creado=creado,db_data=correos)
            else:
                email=form.email.data
                suscrito= False
                db.connect()
                correo=db.fetch_one('SELECT * FROM mails where correo=%s',(email,))
                correos=db.fetch_all('SELECT * FROM mails ORDER BY correo ASC')
                db.close()
                if correo==None:
                    error=f'Correo no existente en la base de datos, puedes agregarlo'
                    return render_template('admin/agregarmails.html', form=form,error=error,db_data=correos)
                if correo[1]==True:
                    db.connect()
                    db.execute('UPDATE mails SET suscrito=%s where correo=%s',(suscrito,email))
                    creado= f'Mail desuscrito exitosamente'
                    correos=db.fetch_all('SELECT * FROM mails ORDER BY correo ASC')
                    db.close()
                    return render_template('admin/agregarmails.html', form=form,creado=creado,db_data=correos)
                else:
                    error= f'Mail ya desuscrito, verifique los datos'
                    return render_template('admin/agregarmails.html', form=form,error=error,db_data=correos)
        else:
            error= f'Datos incorrectos,intente de nuevo'
            db.connect()
            correos=db.fetch_all('SELECT * FROM mails ORDER BY correo ASC')
            db.close()
            return render_template('admin/agregarmails.html', form=form,error=error,db_data=correos)
    db.connect()
    correos=db.fetch_all('SELECT * FROM mails ORDER BY correo ASC')
    db.close()
    return render_template('admin/agregarmails.html', form=form,error=error,db_data=correos)