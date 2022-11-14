from email import message
from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User

# otp = random.randint(100000, 999999)
def send_otp_via_email(email,link):
    subject = f'Verification Link'
    message = f'Your verification link is {link}'
    email_from = settings.EMAIL_HOST
    print(email_from)
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    # user_obj.otp = otp
    user_obj.save()
