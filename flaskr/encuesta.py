from flask import render_template
import flask
from db import get_db_connection
from collections import Counter
import pandas as pd
from __init__ import app

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

@app.route('/verEncuestas')
def rutaDesplegarEncuestas():
    conn = get_db_connection()
    cur = conn.cursor()

    id_encuestas = [1,2,3,4,5,6,7,8] #encuestas a seleccionar

    #creo texto para usar en la sentencias sql seleccionando id de las encuestas con respecto al usuario
    text_id_encuesta = ''
    cantidad_id_encuesta = len(id_encuestas)

    for i in range(cantidad_id_encuesta):
        text_id_encuesta += 'id_encuesta = ' + str(id_encuestas[i])

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

    return render_template('desplegarEncuestas.html', datos=datos)

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

@app.route('/get_word')
def get_prediction():
    id_encuesta = flask.request.args.get('id_encuesta')[0]
    conn = get_db_connection()
    cur = conn.cursor()

    sentenciaSQL = 'SELECT respuesta.respuestas FROM respuesta WHERE respuesta.id_encuesta = ' + id_encuesta + ';'
    cur.execute(sentenciaSQL)
    todas_respuestas = cur.fetchall()
    if(len(todas_respuestas) == 0):
        return flask.jsonify({'porcentajes':'No hay respuestas'})

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
    return flask.jsonify({'porcentajes':porcentajes})

@app.route('/prueba')
def prueba():
    return flask.render_template('prueba.html')
    
@app.route('/agregarmail')
def agregarmail():
    return render_template('agregarmails.html')