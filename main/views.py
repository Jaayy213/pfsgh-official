from django.shortcuts import render

# Home page
def homepage(request):
    context = {

    }
    return render(request, 'main/index.html', context)

# About page
def about(request):
    context = {

    }
    return render(request, 'main/about.html', context)

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
