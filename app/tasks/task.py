from datetime import date , datetime
from app import db , scheduler
import concurrent.futures
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
    today = date.today()
    get_surveys_query = "SELECT id_encuesta,titulo_encuesta FROM encuesta WHERE fecha_comienzo = '{}';".format(str(today))
    list_of_ids_of_surveys = db.fetch_all(get_surveys_query, (today),)
    return parse_list(list_of_ids_of_surveys)


def get_names_of_surveys_start_today():
    """ Obtener los nombres de las encuestas cuya fecha comienzan actualmente """
    today = date.today()
    get_surveys_query = "SELECT titulo_encuesta FROM encuesta WHERE fecha_comienzo = '{}';".format(str(today))
    list_of_names_of_surveys = db.fetch_all(get_surveys_query, (today),)
    return parse_list(list_of_names_of_surveys)



def parse_list(list_of_data):
    """ Extrae el primer elemento de cada tupla dentro de una lista obtenida desde la base de datos """
    return list(map(lambda index: index[0] , list_of_data))


def generate_urls_for_surveys():
    """ Genera las url de todas las encuestas a enviar """
    list_of_ids_of_surveys = get_ids_of_surveys_start_today()
    url_prefix = 'http://152.74.52.191:5004/showSurvey/'

    list_of_urls = []
    for id_survey in list_of_ids_of_surveys:
        url_survey = url_prefix + str(id_survey)
        list_of_urls.append(url_survey)

    return list_of_urls


def generate_complete_email_body():
    """ Funcion que genera el cuerpo del email con todas las encuestas disponibles """
    list_of_titles = get_names_of_surveys_start_today()
    list_of_urls = generate_urls_for_surveys()

    number_of_surveys = len(list_of_titles)

    if number_of_surveys == 0 or list_of_titles is None:
        return None

    email_body = 'Enlaces de encuestas disponibles: \n'

    for index in range(number_of_surveys):
        email_body += f"Encuesta {list_of_titles[index]} : {list_of_urls[index]}\n"
    
    return email_body


def send_async_emails(server , email ,message):
    """ Enviar correos de forma asincrona """
    server.sendmail('mails.empresa.is@gmail.com',email,message)


@scheduler.task("cron",id="async_task",hour=23,minute=30)
def scheduled_send_email_task():
    """ Funcion ejecutada en background para envio de correos masivos """
    start_time = time.time()
    print("Enviando correos de forma asincrona...")
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('mails.empresa.is@gmail.com', 'wctlzgvdtukryohr')

    SUBJECT = "Enlaces de encuestas"

    list_of_emails = get_user_emails()
    email_body = generate_complete_email_body()

    if email_body is None:
        print(f"No hay encuestas habilitadas para el dia de hoy {str(date.today())}")
        return

    message = 'Subject: {}\n\n{}'.format(SUBJECT, email_body)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for email in list_of_emails:
            try:
                executor.map(send_async_emails(server, email, message))
            except Exception as error:
                print("Error la enviar mails " , error)
    
    print(f"Finalizado el proceso de envio de correos asincronos: {time.time() - start_time} segundos")