from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('process/', views.process, name='process'),
    path('services/', views.service, name='services'),
    path('contact/', views.contact, name='contact'),
]
