from django.shortcuts import render

# Create your views here.
def landingpage(request):
    context = {}
    context["content"] = "landingpage.html"

    return render(request, 'base.html', context)