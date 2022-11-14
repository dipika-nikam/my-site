from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,UserBeauticianView,BeauticianRegistrationView,BeauticianphotoView,ServicesView, ContactusView,BeauticianGetView,Paginationview,AddServiceView,ServicesDetailView,BeauticianServiceView,BeauticianDetails

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('change-password/', UserChangePasswordView.as_view(), name = 'change-password'),
    path('reset-password/', SendPasswordResetEmailView.as_view(), name='reset-password'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-beautician/', UserBeauticianView.as_view(), name='user-beautician'),
    path('register-beautician/', BeauticianRegistrationView.as_view(), name='register-beautician'),
    path('beautician-photo/',BeauticianphotoView.as_view(), name='beautician-photo'),
    path('all-service/',ServicesView.as_view(), name='all-service'),
    path('all-servicedetail/',ServicesDetailView.as_view(), name='all-service'),
    path('contact-us/',ContactusView.as_view(), name='contact-us'),
    path('shop/',BeauticianGetView.as_view(), name='shop'),
    path('page/',Paginationview.as_view(), name='pagination'),
    path('service/beautician/',BeauticianServiceView.as_view(), name='test'),
    path('add-service/',AddServiceView.as_view(), name='add-service'),
    path('beautician/details/',BeauticianDetails.as_view(), name='deatils'),
    path('service/beautician/',BeauticianServiceView.as_view(), name='test'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
