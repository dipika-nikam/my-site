from django.urls import path
from .views import AppointmentView,AvailabilitiesView,BeauticianServicesView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('appointment/', AppointmentView.as_view(), name = 'appointment'),
    path('barber-availabilities/', AvailabilitiesView.as_view(), name = 'barber-availabilities'),
    path('barber-services/', BeauticianServicesView.as_view(), name = 'Barberservices')
]
