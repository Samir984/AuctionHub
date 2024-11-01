from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from django.conf import settings


@shared_task
def send_reset_password_email(email, code, first_name):
    subject = "Password Reset Request"
    reset_link = f"http://127.0.0.1:8000/account/reset_password/?code={code}"
    # Render the HTML content
    html_content = render_to_string(
        "password_reset_email.html",
        {"reset_link": reset_link, "first_name": first_name},
    )

    # Create the email message
    email_message = EmailMultiAlternatives(
        subject,
        "Please use an HTML-compatible email client to view this message.",
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
