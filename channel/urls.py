from django.urls import path
from . import views

app_name = 'channel'

urlpatterns = [
    path('<str:channel_id>', views.channel, name='channel'),
]