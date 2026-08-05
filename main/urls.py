from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('client_stories/', views.client_stories, name='client_stories'),
    path('process/', views.process, name='process'),
    path('services/', views.service, name='services'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name="faqs"),
]