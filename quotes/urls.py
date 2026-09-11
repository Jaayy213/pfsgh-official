from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_quote, name='submit_quote'),

    path('dashboard/', views.quote_dashboard, name='quote_dashboard'),
    path('dashboard/<int:pk>/', views.quote_detail, name='quote_detail'),
    path('dashboard/<int:pk>/toggle-processed/', views.toggle_quote_processed, name='toggle_quote_processed'),
    path('dashboard/<int:pk>/delete/', views.delete_quote, name='delete_quote'),
]