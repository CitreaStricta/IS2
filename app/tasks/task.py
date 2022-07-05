from flask import current_app
from flask_mail import Message
from threading import Thread
from smtplib import SMTPException
from .scheduler import scheduler
from app.mail import send_email
from datetime import date, datetime
from app import db,mail


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


def send_async_email(app,message):
    with app.app_context():
        try:
            mail.send(message)
        except SMTPException as err:
            print("Error al enviar email")


def send_email(subject,sender,recipients,text_body,cc=None,bcc=None,html_body=None):
    message = Message(subject,sender=sender,recipients=recipients,cc=cc,bcc=bcc)
    message.body = text_body

    if html_body:
        message.html = html_body

    Thread(target=send_async_email,args=[current_app._get_current_object(),message]).start()
    

@scheduler.task("interval",id="job_sync",seconds=20,max_instances=1,start_date="2022-07-04 12:24:00",)
def scheduled_send_email_task():
    print("Enviando correos de forma asincrona...")
    list_of_urls = generate_urls_for_surveys()
    list_of_emails = get_user_emails()

    for email in list_of_emails:
        for url in list_of_urls:
            send_email(subject='Encuesta para responder',
                    sender='mails.empresa.is@gmail.com',
                    recipients=[email],
                    text_body=f'Hola, puedes contestar la encuesta entrando en: {url}',
                    html_body=None)
    print("Finalizado el proceso de envio de correos asincronos.")
