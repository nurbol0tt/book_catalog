from django.core.mail import send_mail
from django.urls import reverse

from core.celery import app

from apps.user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


@app.task
def send_message_email(email, current_site):
    print(email)
    user = User.objects.filter(email=email).first()
    token = RefreshToken.for_user(user)
    token['email'] = user.email  # Add email to the token payload
    relativeLink = reverse('verify')
    absurl = 'http://' + current_site + relativeLink + "?token=" + str(token.access_token)
    email_body = 'Hi ' + user.username + \
                 ' Use the link below to verify your email \n' + absurl
    send_mail(
        subject='Verify your email',
        message=email_body,
        from_email="settings.EMAIL_HOST_USER",
        recipient_list=[user.email],
    )
