from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BlogCategory, BlogPost, Comment, BlogPageView
from .forms import BlogPostForm, BlogCategoryForm, ProductTagForm, ProductForm
from django.utils import timezone
from django.db.models import Count
from django.utils.timezone import now, timedelta
from enquiries.models import Enquiry
from main.models import ProductTag, Product
from django.db import transaction


# Helper function to get client IP for page views
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
    posts = BlogPost.objects.exclude(slug=slug).order_by('-created_at')
    post = get_object_or_404(BlogPost, slug=slug)
    category_slug = request.GET.get("category")
    comments = post.comments.select_related('user')

    # Track Total Views
    post.total_views += 1
    post.save(update_fields=['total_views'])

    # Track Unique Visitors
    session_key = f'viewed_blog_{post.pk}'
    ip_address = get_client_ip(request)

    if not request.session.get(session_key, False):
        BlogPageView.objects.create(
            post=post,
            ip_address=ip_address,
            session_key=request.session.session_key
        )
        request.session[session_key] = True

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

    today = now()

    # ---------- DAILY (last 7 days) ----------
    daily_start = today - timedelta(days=6)  # 7 days including today
    daily_data = (
        BlogPageView.objects.filter(timestamp__date__gte=daily_start.date())
        .extra({'day': "date(timestamp)"})
        .values('day')
        .annotate(visits=Count('id'))
        .order_by('day')
    )
    daily_labels = [str(d['day']) for d in daily_data]
    daily_values = [d['visits'] for d in daily_data]

    # ---------- WEEKLY (last 4 weeks) ----------
    week_start = today - timedelta(weeks=4)
    weekly_data = (
        BlogPageView.objects.filter(timestamp__date__gte=week_start.date())
        .extra({'week': "strftime('%%Y-%%W', timestamp)"})
        .values('week')
        .annotate(visits=Count('id'))
        .order_by('week')
    )
    weekly_labels = [d['week'] for d in weekly_data]
    weekly_values = [d['visits'] for d in weekly_data]

    # ---------- MONTHLY (last 12 months) ----------
    month_start = today - timedelta(days=365)
    monthly_data = (
        BlogPageView.objects.filter(timestamp__date__gte=month_start.date())
        .extra({'month': "strftime('%%Y-%%m', timestamp)"})
        .values('month')
        .annotate(visits=Count('id'))
        .order_by('month')
    )
    monthly_labels = [d['month'] for d in monthly_data]
    monthly_values = [d['visits'] for d in monthly_data]

    # Total visitors
    total_visitors = BlogPageView.objects.count()
    monthly_visitors = BlogPageView.objects.filter(timestamp__gte=today - timedelta(days=30)).count()
    weekly_visitors = BlogPageView.objects.filter(timestamp__gte=today - timedelta(days=7)).count()
    daily_visitors = BlogPageView.objects.filter(timestamp__gte=today - timedelta(days=1)).count()

    # Recent Enquiries
    recent_enquiries = Enquiry.objects.order_by('-created_at')[:5]

    context = {
        'posts': posts,
        'total_posts': total_posts,
        'total_categories': total_categories,
        'total_comments': total_comments,
        'daily_labels': daily_labels,
        'daily_values': daily_values,
        'weekly_labels': weekly_labels,
        'weekly_values': weekly_values,
        'monthly_labels': monthly_labels,
        'monthly_values': monthly_values,
        'daily_visitors': daily_visitors,
        'weekly_visitors': weekly_visitors,
        'monthly_visitors': monthly_visitors,
        'total_visitors': total_visitors,
        'recent_enquiries': recent_enquiries,
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
    categories = BlogCategory.objects.annotate(
        post_count=Count('posts')
    ).order_by('-created_at')

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
        form = BlogCategoryForm()

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
def product_tags(request):
    tags = ProductTag.objects.annotate(
        product_count=Count('product_tags')
    ).order_by('-created_at')

    context = {
        'tags': tags,
    }

    return render(request, 'blog/dashboard/product_tags.html', context)


@staff_member_required
@login_required
def create_product_tag(request):
    if request.method == 'POST':
        form = ProductTagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Tag created successfully!")
            return redirect('product_tags')
    else:
        form = ProductTagForm()

    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'blog/dashboard/product_tag_form.html', context)


@staff_member_required
@login_required
def edit_product_tag(request, pk):
    tag = get_object_or_404(ProductTag, pk=pk)

    if request.method == 'POST':
        form = ProductTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Tag updated successfully!")
            return redirect('product_tags')
    else:
        form = ProductTagForm(instance=tag)
    
    context = {
        'form': form,
        'tag': tag,
        'is_edit': True,
    }

    return render(request, 'blog/dashboard/product_tag_form.html', context)


@staff_member_required
@login_required
def delete_product_tag(request, pk):
    tag = get_object_or_404(ProductTag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, "Product Tag deleted successfully!")
        return redirect('product_tags')
    return render(request, 'blog/dashboard/product_tag_form.html')


@login_required
@staff_member_required
def product_list(request):
    products = Product.objects.select_related('tag').all().order_by('-created_at')
    context = {
        'products': products,
    }
    return render(request, 'blog/dashboard/product_list.html', context)


@login_required
@staff_member_required
@transaction.atomic
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # request.FILES is required for ImageField!
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'is_edit': False,
    }
    
    return render(request, 'blog/dashboard/product_form.html', context)


@login_required
@staff_member_required
@transaction.atomic
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'is_edit': True,
        'product': product,
    }
        
    return render(request, 'blog/dashboard/product_form.html', context)


@login_required
@staff_member_required
@transaction.atomic
def delete_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' deleted successfully!")
    return redirect('product_list')


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