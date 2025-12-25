from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog, name='blog'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),

    # path('dashboard/home/', views.dashboard_home, name='dashboard_home'),
    # path('dashboard/posts/', views.post_list, name='post_list'),
    # path('dashboard/posts/create/', views.create_post, name='post_create'),
    # path('dashboard/posts/<int:pk>/edit/', views.edit_post, name='post_edit'),
    # path('dashboard/posts/<int:pk>/delete/', views.delete_post, name='post_delete'),

    path('dashboard/home/', views.blog_dashboard, name='blog_dashboard'),
    path('dashboard/blog_posts/', views.blog_posts_list, name='blog_posts_list'),
    path('dasbhoard/blog_categories/', views.blog_categories, name='blog_categories'),
    path('dashboard/blog_posts_comments/', views.blog_posts_comments, name='blog_posts_comments'),
    path('dashboard/delete_blog_post_comments/<int:pk>/', views.delete_blog_post_comment, name='delete_comment'),
    path('dashboard/create_blog_post/', views.create_blog_post, name='create_blog_post'),
    path('dashboard/edit_blog_post/<slug:slug>/', views.edit_blog_post, name='edit_blog_post'),
    path('dashboard/delete_blog_post/<slug:slug>/', views.delete_blog_post, name='delete_blog_post'),
    path('dashboard/create_category/', views.create_category, name='create_category'),
    path('dashboard/edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('dashboard/delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('dashboard/user_profile/', views.user_profile, name='user_profile'),
]
