from sendit.apps.core.celery import app

from .sendmail import SendMail


@app.task(name="mail_handler")
def mail_handler(template, email_data, mail_subject, mails):
    context = {
        "title": email_data[0],
        "message_body": email_data[1],
        "button_action": email_data[4],
        "name": email_data[3],
        "verification_link": email_data[2],
    }
    return SendMail(template, context, mail_subject, mails).send()
