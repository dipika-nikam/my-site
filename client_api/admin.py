from django.contrib import admin
from .models import AppointmentModel,BeauticianAvailabilities,BeauticianServices

# # Register your models here.
admin.site.register(AppointmentModel)
admin.site.register(BeauticianAvailabilities)
admin.site.register(BeauticianServices)
