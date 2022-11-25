from email import message
from django.core.mail import send_mail
from django.template.loader import get_template
import random
from django.conf import settings
from .models import User

# otp = random.randint(100000, 999999)
def send_otp_via_email(email,link):
    subject = f'Verification Link'
    message = f'Your verification link is {link}'
    email_from = settings.EMAIL_HOST
    print(email_from)
    context = {
        'link': link,
        'email': email,
    }
    template = get_template('email.html').render(context)
    send_mail(subject, None, email_from, [email],fail_silently=False,html_message=template)
    user_obj = User.objects.get(email=email)
    # user_obj.otp = otp
    user_obj.save()
