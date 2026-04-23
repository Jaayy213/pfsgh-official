from django.urls import path
from . import views

urlpatterns = [
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('success/', views.enquiry_success, name='enquiry_success'),
    path("update-status/", views.update_enquiry_status, name="update_enquiry_status"),
]
