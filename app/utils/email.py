from flask_mail import Message
from flask import current_app,render_template

def send_email(to,subject,template,**kw):
    msg = Message(current_app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject, \
                    sender = current_app.config['FLASK_MAIL_SENDER'], \
                    recipients = [to])
    msg.body = render_template(template + ".txt",**kw)
    msg.html = render_template(template + ".html",**kw)
    mail.send(msg)

