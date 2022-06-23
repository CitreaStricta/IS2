from . import surveys_bp
from flask import render_template, url_for, request, jsonify,redirect
from app import db
from datetime import date
import json

@surveys_bp.route("/showSurvey/<id>")
def showSurvey(id):
    survey_structure = db.fetch_one(f"SELECT * FROM encuesta WHERE id_encuesta = {id}") #cambiar a dinamico

    if survey_structure is None:
        return render_template("surveys/alert.html")

    start_date_of_survey = survey_structure[3]
    end_date_of_survey = survey_structure[4]

    #Encuesta aun no habilitada
    if start_date_of_survey > date.today():
        return render_template("surveys/notEnabled.html",endedSurvey=False)
    elif end_date_of_survey < date.today():
        #Encuesta finalizó su periodo de habilitacion
        return render_template("surveys/notEnabled.html",endedSurvey=True)
        

    survey_title = survey_structure[1]
    survey_description = survey_structure[2]
    survey_questions = survey_structure[5][0]
    
    questions = []
    choices = []
    for question_index,data in enumerate(survey_questions):
        questions.append(data['Pregunta'])

        alternatives = []
        for alternative_number,alternative in enumerate(data['Alternativas']):
            #Crear tuplas con numero de alternativa y valor de alternativa
            alternatives.append(alternative)
        choices.append(alternatives)

    return render_template("surveys/showSurvey.html",idSurvey=id, questions=questions,choices=choices ,surveyTitle=survey_title, surveyDescription=survey_description)



@surveys_bp.route("/saveSurveyAnswer/<id>", methods=['POST'])
def saveSurveyAnswer(id):
    if request.method == 'POST':
        datosEncuesta = request.get_json(force = True)
        id_encuesta = id
        #id_encuestado = datosEncuesta[1]
        id_encuestado = 1 #Esperar a cambio en la tabla
        fecha = date.today()

        #return {"hola": "mundo!"} 

        try: 
            sql = 'INSERT INTO respuesta (id_respuesta, id_encuesta, id_encuestado, fecha, respuestas) VALUES (DEFAULT,%s,%s,%s,%s)'
            db.execute(sql, (id_encuesta,id_encuestado,fecha,json.dumps(datosEncuesta[0])))
        except Exception as e:
            print(e)
            return {"message": "error!"}

    return {"hola": "mundo!"}     


@surveys_bp.route("/success")
def success():
    return render_template("surveys/success.html")