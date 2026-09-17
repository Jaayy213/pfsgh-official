from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.service_request_view, name='service_request'),
]