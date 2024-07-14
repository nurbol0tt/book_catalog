from django.core.mail import send_mail

from src.core.celery import app


@app.task
def send_message_email(data):
    email_body = "Hi, it is your login and password from the account, don't show it to anyone\n" + \
                 f"Login: {data.email}" + f" Password: {data.password}"
    send_mail("Adding you to the program",
              email_body,
              "settings.EMAIL_HOST_USER",
              [data.email]
              )
