from django.shortcuts import render

# Blog page
def blog(request):
    context = {

    }
    return render(request, 'main/blog.html', context)