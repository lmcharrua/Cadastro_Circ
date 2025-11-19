from django.urls import path
from . import views

urlpatterns = [
    path('lista_sdados', views.lista_sdados, name='lista_sdados'),
    path('criar_sdados', views.criar_sdados, name='criar_sdados'),
    path('editar_sdados/<int:pk>/', views.editar_sdados, name='editar_sdados'),
    path('editar_sterm/<int:pk>/', views.editar_sterm, name='editar_sterm'),
    path('criar_sterm', views.criar_sterm, name='criar_sterm'),

    path('lsdados', views.lsdados, name='lsdados'),
    path('csdados', views.csdados, name='csdados'),
    path('esdados/<int:pk>/', views.esdados, name='esdados'),
    path('esterm/<int:pk>/', views.esterm, name='esterm'),
    path('csterm', views.csterm, name='csterm'),
]