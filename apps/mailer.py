from mailer import Mailer, Message

from config import Config

def send_email(mailto, subject, template, template_context):
    """ Shortcut to send emails """
    message = Message(From=Config.MAILER['email'],
                      To=mailto,
                      charset="utf-8")
    message.Subject = """Make A Stand! Lemon-aid / %s""" % subject
    message.Body = template('mail/%s.html' % template, **template_context)

    sender = Mailer(
        host=Config.MAILER['host'],
        port=Config.MAILER['port'],
        use_tls=Config.MAILER['use_tls'],
        usr=Config.MAILER['user'],
        pwd=Config.MAILER['password']
    )
    return sender.send(message)

