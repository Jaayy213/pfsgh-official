from django.urls import path
from . import views


urlpatterns = [
    path('product_launch/', views.product_launch, name='product_launch'),
    path('product_launch/rsvp', views.rsvp_view, name='rsvp_submit'),
]