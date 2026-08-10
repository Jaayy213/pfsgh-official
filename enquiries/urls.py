from django.urls import path
from . import views

urlpatterns = [
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('success/', views.enquiry_success, name='enquiry_success'),
    path("update-status/", views.update_enquiry_status, name="update_enquiry_status"),
    path("enquiry/add_comment/<int:pk>/", views.create_comment, name="add_enquiry_comment"),
    path("enquiry/update_comment/<int:pk>/", views.update_comment, name="update_enquiry_comment"),
    path("enquiry/delete_comment/<int:pk>/", views.delete_comment, name="delete_enquiry_comment"),
]
