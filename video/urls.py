from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    path('<str:video_id>', views.video, name='video'),
]