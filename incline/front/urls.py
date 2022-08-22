from django.urls import path
from . import views

urlpatterns = [
    path('docs/', views.docs, name='docs'),
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
]