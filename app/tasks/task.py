from flask import current_app
from app.mail import send_email
from datetime import date , datetime
from app import db , scheduler
import time
import smtplib


def get_user_emails():
    """ Obtener los emails de los usuarios que estan suscritos """
    get_emails_query = 'SELECT correo FROM mails WHERE mails.suscrito = True;'
    list_of_emails = db.fetch_all(get_emails_query)
    list_of_emails = [index[0] for index in list_of_emails]
    return list_of_emails


def get_ids_of_surveys_start_today():
    """ Obtener los id de las encuestas cuya fecha comienzan actualmente """
    today = '2022-06-06'#date.today() dejar como fecha actual , fecha hardcodeada es solo motivo de prueba
    get_surveys_query = "SELECT id_encuesta FROM encuesta WHERE fecha_comienzo = '{}';".format(str(today))
    list_of_ids_of_surveys = db.fetch_all(get_surveys_query, (today),)
    return parse_list_of_ids(list_of_ids_of_surveys)


def parse_list_of_ids(list_of_ids):
    """ Extrae el id de cada tupla dentro de una lista obtenida desde la base de datos """
    return list(map(lambda index: index[0] , list_of_ids))


def generate_urls_for_surveys():
    """ Genera las url de todas las encuestas a enviar """
    list_of_ids_of_surveys = get_ids_of_surveys_start_today()
    url_prefix = 'http://127.0.0.1:5004/showSurvey/'

    list_of_urls = []
    for id_survey in list_of_ids_of_surveys:
        url_survey = url_prefix + str(id_survey)
        list_of_urls.append(url_survey)

    return list_of_urls
    

@scheduler.task("interval",id="job_sync",seconds=100,max_instances=1,start_date="2022-07-04 12:24:00",)
def scheduled_send_email_task():
    print("Enviando correos de forma asincrona...")
    list_of_urls = generate_urls_for_surveys()
    list_of_emails = get_user_emails()

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('mails.empresa.is@gmail.com', 'wctlzgvdtukryohr')

    SUBJECT = "Enlace de encuesta"
    TEXT = "El enlace de la encuesta es el siguiente, gracias por responder: "

    start_time = time.time()
    for email in list_of_emails:
        for url in list_of_urls:
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT + url)
            try:
                server.sendmail('mails.empresa.is@gmail.com', email, message)
            except Exception as error:
                print("Error al enviar correo electronico: " , error)
    print(f"Finalizado el proceso de envio de correos asincronos: {time.time() - start_time} segundos")