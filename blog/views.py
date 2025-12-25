from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BlogCategory, BlogPost, Comment
from .forms import BlogPostForm, BlogCategoryForm
from django.utils import timezone

# Blog Homepage
def blog(request):
    category_slug = request.GET.get("category")
    posts = BlogPost.objects.all().order_by('-created_at')
    query = request.GET.get('q', '')

    # Filter by category
    if category_slug:
        posts = posts.filter(category__name__iexact=category_slug)

    # Search articles
    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = BlogCategory.objects.all()
    featured_post = BlogPost.objects.filter(is_featured=True).order_by('-created_at').first()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "featured_post": featured_post,
        "selected_category": category_slug,
        "query": query,
    }

    return render(request, 'blog/blog_home.html', context)

# Blog Detail Page
def blog_detail(request, slug):
    posts = BlogPost.objects.all().order_by('-created_at')
    post = get_object_or_404(BlogPost, slug=slug)
    category_slug = request.GET.get("category")
    comments = post.comments.select_related('user')

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')

        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            messages.success(request, "Comment added successfully.")
            return redirect('blog_detail', slug=slug)

    # Filter by category
    if category_slug:
        posts = posts.filter(category__name__iexact=category_slug)
    
    categories = BlogCategory.objects.all()

    context = {
        "posts": posts,
        "post": post,
        "categories": categories,
        "comments": comments,
    }

    return render(request, "blog/blog_detail.html", context)



# BLOG DASHBOARD
@staff_member_required
@login_required
def blog_dashboard(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    total_posts = posts.count()
    total_categories = BlogCategory.objects.all().count()
    total_comments = Comment.objects.all().count()

    context = {
        'posts': posts,
        'total_posts': total_posts,
        'total_categories': total_categories,
        'total_comments': total_comments,
    }

    return render(request, 'blog/dashboard/dashboard_home.html', context)

@staff_member_required
@login_required
def blog_posts_list(request):
    posts = BlogPost.objects.all().order_by('-updated_at')

    context = {
        'posts': posts,
    }

    return render(request, 'blog/dashboard/post_list.html', context)

@staff_member_required
@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog Post created successfully!")
            return redirect('blog_posts_list')
    else:
        form = BlogPostForm()
    
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'blog/dashboard/post_form.html', context)

@staff_member_required
@login_required
def edit_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog Post updated successfully!")
            return redirect('blog_posts_list')
    else:
        form = BlogPostForm(instance=post)
    
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'blog/dashboard/post_form.html', context)

@staff_member_required
@login_required
def delete_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Blog Post deleted successfully!")
        return redirect('blog_posts_list')
    return render(request, 'blog/dashboard/post_list.html')

@staff_member_required
@login_required
def blog_categories(request):
    categories = BlogCategory.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'blog/dashboard/categories.html', context)

@staff_member_required
@login_required
def create_category(request):
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('blog_categories')
    else:
        form = BlogCategory()

    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'blog/dashboard/category_form.html', context)

@staff_member_required
@login_required
def edit_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)

    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('blog_categories')
    else:
        form = BlogCategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'is_edit': True,
    }

    return render(request, 'blog/dashboard/category_form.html', context)

@staff_member_required
@login_required
def delete_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('blog_categories')
    return render(request, 'blog/dashboard/categories.html')

@staff_member_required
@login_required
def blog_posts_comments(request):
    comments = Comment.objects.select_related('user', 'post').order_by('-created_at')

    context = {
        'comments': comments,
    }

    return render(request, 'blog/dashboard/comments.html', context)

@staff_member_required
def delete_blog_post_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('blog_posts_comments')
    return render(request, 'blog/dashboard/comments.html')

@staff_member_required
@login_required
def user_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_profile":
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            profile.phone = request.POST.get("phone")
            user.save()
            profile.save()
            messages.success(request, "Profile updated successfully.")

        elif action == "update_avatar":
            if "avatar" in request.FILES:
                profile.image = request.FILES["avatar"]
                profile.save()
                messages.success(request, "Profile picture updated.")

        elif action == "change_password":
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                request.user.profile.last_password_change = timezone.now()
                request.user.profile.save()
                messages.success(request, "Password updated successfully.")
            else:
                messages.error(request, "Password update failed.")

        return redirect("user_profile")

    return render(request, 'blog/dashboard/user_profile.html')