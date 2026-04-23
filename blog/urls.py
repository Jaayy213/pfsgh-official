from django.urls import path
from . import views
from enquiries.views import enquiry_dashboard, export_enquiries


urlpatterns = [
    # Blog Page
    path('', views.blog, name='blog'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Dashboard (Blog)
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

    # Dashboard (Enquiries)
    path("dashboard/enquiries/", enquiry_dashboard, name="enquiry_dashboard"),
    path("dashboard/enquiries/export/", export_enquiries, name="export_enquiries"),
]
