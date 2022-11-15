from django.contrib import admin
from .models import AppointmentModel,BeauticianAvailabilities,BeauticianServices,Ratingmodel,Blogmodel

# # Register your models here.
admin.site.register(AppointmentModel)
admin.site.register(BeauticianAvailabilities)
admin.site.register(BeauticianServices)
admin.site.register(Ratingmodel)
admin.site.register(Blogmodel)
