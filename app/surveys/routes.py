from . import surveys_bp
from flask import render_template, url_for, request, jsonify
from app import db

@surveys_bp.route("/showSurvey/<id>")
def showSurvey(id):
    survey_structure = db.fetch_one(f"SELECT * FROM encuesta WHERE id_encuesta = {id}") #cambiar a dinamico

    if survey_structure is None:
        return render_template("surveys/alert.html")

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

    return render_template("surveys/showSurvey.html",questions=questions,choices=choices ,surveyTitle=survey_title, surveyDescription=survey_description)



@surveys_bp.route("/saveSurveyAnswer/<id>", methods=['POST'])
def saveSurveyAnswer():
    pass