from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, AudioFile, VideoFile
from .forms import AudioUploadForm, VideoUploadForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
import datetime




# Home page
def homepage(request):
    welcome_audio = AudioFile.objects.order_by('-created_at').first()

    # PRODUCT LAUNCH RSVP Expiry set to Sept 25, 2026 end-of-day
    event_expiry = timezone.make_aware(datetime.datetime(2026, 9, 25, 23, 59, 59))
    show_rsvp_banner = timezone.now() <= event_expiry

    context = {
        'welcome_audio': welcome_audio,
        'show_rsvp_banner': show_rsvp_banner,
    }
    return render(request, 'main/index.html', context)

# About page
def about(request):
    context = {

    }
    return render(request, 'main/about.html', context)

# Client Stories
def client_stories(request):
    products = Product.objects.all()
    # fetch products with same tags
    # products = Product.objects.select_related('tag').all()

    context = {
        'products': products,
    }
    return render(request, 'main/client_stories.html', context)

# Process page
def process(request):
    context = {

    }
    return render(request, 'main/process.html', context)

# Services page
def service(request):
    context = {

    }
    return render(request, 'main/service.html', context)

# FAQs page
def faqs(request):
    context = {

    }
    return render(request, 'main/faqs.html', context)

# Contact page
def contact(request):
    context = {

    }
    return render(request, 'main/contact.html', context)


# Privacy Policy page
def privacy(request):
    context = {

    }
    return render(request, 'main/privacy.html', context)


# Terms of Service page
def terms(request):
    context = {

    }
    return render(request, 'main/terms.html', context)


# Central Login Page
def pfs_connect(request):
    context = {

    }
    return render(request, 'main/pfs_connect.html', context)


# Audio List & Upload View
@login_required
def manage_audio(request):
    audio_files = AudioFile.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_audio')
    else:
        form = AudioUploadForm()

    context = {
        'audio_files': audio_files,
        'form': form,
    }
        
    return render(request, 'blog/dashboard/audio_list.html', context)


# Video List & Upload View
@login_required
def manage_video(request):
    video_files = VideoFile.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_video')
    else:
        form = VideoUploadForm()

    context = {
        'video_files': video_files,
        'form': form
    }
        
    return render(request, 'blog/dashboard/video_list.html', context)


@login_required
@require_POST
def delete_audio(request, pk):
    audio = get_object_or_404(AudioFile, pk=pk)
    audio.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def delete_video(request, pk):
    video = get_object_or_404(VideoFile, pk=pk)
    video.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def edit_audio(request, pk):
    audio = get_object_or_404(AudioFile, pk=pk)
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES, instance=audio)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{audio.title}' updated successfully.")
        else:
            messages.error(request, "Failed to update audio. Please check your inputs.")
    return redirect('manage_audio')


@login_required
@require_POST
def edit_video(request, pk):
    video = get_object_or_404(VideoFile, pk=pk)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{video.title}' updated successfully.")
        else:
            messages.error(request, "Failed to update video. Please check your inputs.")
    return redirect('manage_video')