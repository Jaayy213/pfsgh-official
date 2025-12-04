from django.shortcuts import render

# Blog page
def blog(request):
    context = {

    }
    return render(request, 'blog/blog_home.html', context)