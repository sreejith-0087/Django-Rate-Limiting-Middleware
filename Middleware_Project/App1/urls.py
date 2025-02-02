from django.urls import path
from . import views


urlpatterns = [
    path('', views.count_view, name='count_view'),
]