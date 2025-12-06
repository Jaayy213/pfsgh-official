from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import BlogCategory, BlogPost
from .forms import BlogPostForm

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
    post = get_object_or_404(BlogPost, slug=slug)

    context = {
        "post": post,
    }

    return render(request, "blog/blog_detail.html", context)


# BLOG DASHBOARD
# Dashboard Landing Page
# @login_required(login_url='login')
def dashboard_home(request):
    featured_post = BlogPost.objects.filter(is_featured=True).first()

    context = {
        'featured_post': featured_post,
    }

    return render(request, 'blog/dashboard/dashboard_home.html', context)


# List all blog posts
@login_required(login_url='login')
def post_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'blog/dashboard/post_list.html', context)


# Create a new blog post
@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # if author exists in BlogPost model
            post.save()
            return redirect('dashboard:post_list')
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }

    return render(request, 'blog/dashboard/create_post.html', context)


# Edit an existing blog post
@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard:post_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/dashboard/edit_post.html', {'form': form, 'post': post})


# Delete a blog post (with confirmation)
@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('dashboard:post_list')
    return render(request, 'blog/dashboard/delete_post.html', {'post': post})
