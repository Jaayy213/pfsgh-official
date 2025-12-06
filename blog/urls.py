from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog, name='blog'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),

    path('dashboard/home/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/posts/', views.post_list, name='post_list'),
    path('dashboard/posts/create/', views.create_post, name='post_create'),
    path('dashboard/posts/<int:pk>/edit/', views.edit_post, name='post_edit'),
    path('dashboard/posts/<int:pk>/delete/', views.delete_post, name='post_delete'),
]
