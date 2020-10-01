import logging
import os
import smtplib

from smtplib import SMTPResponseException
from email.message import EmailMessage

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    sec_form   = req_body.get('sec_form')
    if ( sec_form is None or type(sec_form) != str ):
        return func.HttpResponse(
            "Error on sec_form argument",
            status_code=404
        )

    firstname   = req_body.get('firstname')
    if ( firstname is None or type(firstname) != str ):
        return func.HttpResponse(
            "Error on firstname argument",
            status_code=400
        )

    lastname    = req_body.get('lastname')
    if ( lastname is None or type(lastname) != str ):
        return func.HttpResponse(
            "Error on lastname argument",
            status_code=400
        )

    phone       = req_body.get('phone')
    if ( phone is None or type(phone) != str ):
        return func.HttpResponse(
            "Error on phone argument",
            status_code=400
        )

    email       = req_body.get('email')
    if ( email is None or type(email) != str ):
        return func.HttpResponse(
            "Error on email argument",
            status_code=400
        )

    message     = req_body.get('message')
    if ( message is None or type(message) != str ):
        return func.HttpResponse(
            "Error on message argument",
            status_code=400
        )

    msg = EmailMessage()
    msg['From'] = os.environ["smtp_user"]
    msg['To'] = '%s, %s' %(os.environ["mail_dest"], email)
    msg.add_header('reply-to', email)
    msg.add_header('Content-Type','text/html')
    msg['Subject'] = 'Contact depuis le site %s : %s' %(os.environ["Company"], email)
    msg.set_content("""\
Bonjour %s !

Contact depuis le site %s !

Nom : %s
Prénom : %s 
Numéro de téléphone : %s
E-mail : %s
Message : %s

""" %(os.environ["Company"], os.environ["Company_Website"], firstname, lastname, phone, email, message))

    try:
        smtpserver = smtplib.SMTP(os.environ["smtp_host"], os.environ["smtp_port"])
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(os.environ["smtp_user"], os.environ["smtp_pass"])
        smtpserver.send_message (msg)
        smtpserver.close()
        return func.HttpResponse(
            "Mail sent!",
            status_code=200
        )

    except SMTPResponseException as e:
        return func.HttpResponse(
            "Error sending mail! error_code: %d, error_message: %s" %(e.smtp_code, e.smtp_error),
            status_code=500
        )