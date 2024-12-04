from django.shortcuts import render

# Create your views here.
def video(request, video_id):
    context = {}

    context["content"] = "video.html"

    return render(request, 'base.html', context)
