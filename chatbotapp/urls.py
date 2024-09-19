from django.urls import path
from . import views

urlpatterns = [
  path('', views.TopView.as_view(), name='index'),
  path('bot_response', views.bot_response, name='bot_response')
]