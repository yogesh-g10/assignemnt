from django.core.mail import EmailMultiAlternatives

from Assignment1 import settings


def trigger_email(kwargs):
    subject = kwargs['subject']
    body = kwargs['body']
    recipients = kwargs['recipients']
    bcc = kwargs.get('bcc')
    html_content = kwargs.get('template')
    attachments = kwargs.get('attachments')

    if not isinstance(recipients, list):
        recipients = [recipients]

    email = EmailMultiAlternatives(
        subject, body, settings.EMAIL_HOST,
        recipients, bcc,
    )
    if attachments:
        for file_path in attachments:
            email.attach_file(file_path)
    if html_content:
        email.attach_alternative(html_content, "text/html")

    email.send()