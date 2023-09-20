from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from blog.models import Event, AppUser, Employee


def send_email(*args, **kwargs):
    event_type = kwargs['event_type']
    event = kwargs['instance_id']
    instance = Event.objects.get(id=event)
    if event_type == Event.EventType.office:
        template = 'office_meet.html'
    else:
        template = 'party.html'

    subject = 'Invitation'
    # email template included in templates/contact/  to send html email.
    message = render_to_string(template, {})
    from_email = "kiratwadyogesh@gmail.com"
    for user in AppUser.objects.all():
        to_email = user.email
        if not to_email:
            continue
        email = EmailMessage(
            subject, message, from_email=from_email, to=[to_email]
        )
        email.content_subtype = "html"

        email.send()
        Employee.objects.create(user=user, event=instance, mail_status=True)
    return "Done"
