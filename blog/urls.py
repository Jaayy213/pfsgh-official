from django.urls import path
from . import views
from enquiries.views import enquiry_dashboard, export_enquiries
from main.views import manage_audio, manage_video, edit_audio, edit_video, delete_audio, delete_video
from events.views import rsvp_dashboard, rsvp_delete, rsvp_edit


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

    # RSVP (Product Launch)
    path('dashboard/rsvps/', rsvp_dashboard, name='rsvp_dashboard'),
    path('dashboard/rsvps/<int:pk>/edit/', rsvp_edit, name='rsvp_edit'),
    path('dashboard/rsvps/<int:pk>/delete/', rsvp_delete, name='rsvp_delete'),

    # Product Tags & Products
    path('dashboard/product_tags', views.product_tags, name='product_tags'),
    path('dashboard/create_product_tag', views.create_product_tag, name='create_product_tag'),
    path('dashboard/edit_product_tag/<int:pk>/', views.edit_product_tag, name='edit_product_tag'),
    path('dashboard/delete_product_tag/<int:pk>/', views.delete_product_tag, name='delete_product_tag'),

    path('dashboard/products/', views.product_list, name='product_list'),
    path('dashboard/products/create/', views.create_product, name='create_product'),
    path('dashboard/products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('dashboard/products/delete/<int:pk>/', views.delete_product, name='delete_product'),

    # Manage Audio and Video Files
    path('dashboard/audios/', manage_audio, name='manage_audio'),
    path('dashboard/videos/', manage_video, name='manage_video'),
    path('dashboard/audios/edit/<int:pk>/', edit_audio, name='edit_audio'),
    path('dashboard/videos/edit/<int:pk>/', edit_video, name='edit_video'),
    path('dashboard/audios/delete/<int:pk>/', delete_audio, name='delete_audio'),
    path('dashboard/videos/delete/<int:pk>/', delete_video, name='delete_video'),
]
