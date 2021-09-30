from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
]
