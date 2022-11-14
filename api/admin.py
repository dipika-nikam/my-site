from django.contrib import admin
from .models import User, Beautician, Service, Beauticianphoto,Contactus
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

admin.site.register(User)
admin.site.register(Beautician)
admin.site.register(Service)
admin.site.register(Beauticianphoto)
admin.site.register(Contactus)
