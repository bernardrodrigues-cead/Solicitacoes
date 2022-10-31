from django.conf import settings
from django.core.mail import send_mail

class SendEmail(object):
    def __init__(self, subject=None, message=None, email_from=settings.EMAIL_HOST_USER, recipients=None):
        self.subject = subject
        self.message = message
        self.emailfrom = email_from
        self.recipients = recipients

    def send(self):
        return send_mail(self.subject, self.message, self.emailfrom, self.recipients)