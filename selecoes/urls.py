from django.urls import path
from .views import home

urlpatterns = [
    path('', home),
    path('selecoes/tests', home, name='home'),
]