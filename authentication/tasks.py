from django.core.mail import send_mail
from django.conf import settings

def send_email(email: str, username: str, message: str) -> None:
    send_mail(
        subject="Congrats new member",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True
    )