from datetime import datetime
from mailer import Mailer, Message

from datafly.core import template

from config import Config, db


def send_email(mailto, subject, template_name, template_context=None, premailer=True):
    """ Shortcut to send emails """
    message = Message(From=Config.MAILER['email'],
                      To=mailto,
                      charset="utf-8")
    message.Subject = subject = """%s / %s""" % (Config.WEBSITE, subject)
    if template_context is None:
        template_context = {}
    template_context['subject'] = subject
    template_context['base_url'] = Config.BASE_URL
    html = template('mail/%s.html' % template_name, **template_context)
    if premailer:
        from premailer import transform
        html = transform(html)
    message.Html = html

    sender = Mailer(
        host=Config.MAILER['host'],
        port=Config.MAILER['port'],
        use_tls=Config.MAILER['use_tls'],
        usr=Config.MAILER['user'],
        pwd=Config.MAILER['password']
    )
    if Config.__name__ != 'Production':
        db.testmail.insert({
            'mailto': mailto,
            'subject': subject,
            'html': html,
            'sent_at': datetime.utcnow()
        })
        return True
    else:
        return sender.send(message)