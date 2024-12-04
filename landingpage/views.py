from django.shortcuts import render

# Create your views here.
def landingpage(request):
    context = {}
    context["content"] = "landingpage.html"

    return render(request, 'base.html', context)

def detailpage(request):
    context = {}
    context["content"] = "detail.html"

    return render(request, 'base.html', context)