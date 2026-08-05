from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, AudioFile, VideoFile
from .forms import AudioUploadForm, VideoUploadForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages


# Home page
def homepage(request):
    welcome_audio = AudioFile.objects.order_by('-created_at').first()
    context = {
        'welcome_audio': welcome_audio,
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


from django.shortcuts import render, redirect


# Audio List & Upload View
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


@require_POST
def delete_audio(request, pk):
    audio = get_object_or_404(AudioFile, pk=pk)
    audio.delete()
    return JsonResponse({'success': True})


@require_POST
def delete_video(request, pk):
    video = get_object_or_404(VideoFile, pk=pk)
    video.delete()
    return JsonResponse({'success': True})



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