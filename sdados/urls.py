from django.urls import path
from . import views

urlpatterns = [
    path('lista_sdados', views.lista_sdados, name='lista_sdados'),
    path('criar_sdados/<int:pk>/', views.criar_sdados, name='criar_sdados'),
    path('editar_sdados/<int:pk>/', views.editar_sdados, name='editar_sdados'),
    path('editar_sterm/<int:pk>/', views.editar_sterm, name='editar_sterm'),
    path('criar_sterm/<int:pk>/', views.criar_sterm, name='criar_sterm'),

]