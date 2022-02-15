from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca', views.busca, name='busca'),
    path('resultado',views.resultado,name='resultado'),
    path('relacao',views.relacao,name='relacao'),
]