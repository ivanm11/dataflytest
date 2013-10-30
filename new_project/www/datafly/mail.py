from datetime import datetime
from mandrill import Mandrill

from datafly.core import template

from config import Config, db


def send_email(mailto, subject, template_name, template_context=None, premailer=True):
    """ Shortcut to send emails """
    subject = """%s / %s""" % (Config.WEBSITE, subject)
    if template_context is None:
        template_context = {}
    template_context['subject'] = subject
    template_context['base_url'] = Config.BASE_URL
    html = template(template_name if 'html' in template_name else
                    'mail/%s.html' % template_name, **template_context)
    if premailer:
        from premailer import transform
        html = transform(html)
    try:
        if Config.ENV != 'Production':
            raise Exception("Sent real emails only in Production env")
        mc = Mandrill(Config.MANDRILL_API_KEY)
        message = {
            'to': [{'email': mailto}],
            'from_email': Config.EMAIL,
            'from_name': Config.WEBSITE,
            'subject': subject,
            'html': html
        }
        mc.messages.send(message = message)
        return { 'error': False }
    except:
        log_msg = {
            'mailto': mailto,
            'subject': subject,
            'html': html,
            'sent_at': datetime.now()
        }
        db.testmail.insert(log_msg)