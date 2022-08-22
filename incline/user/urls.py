from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('help/', views.help, name='help'),
    path('register_user/', views.register_user, name='register'),
    path('contracts/<int:contractnumber>', views.contracts, name='contracts'),
    path('new_contract/', views.new_contract, name='new_contract'),
]