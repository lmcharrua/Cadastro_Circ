""" from django.urls import path
from . import views

urlpatterns = [
    path('lista_sdados', views.lista_sdados, name="lista_sdados"),
    path('detalhe_sdados/<int:pk>', views.detalhe_sdados, name="detalhe_sdados"),
    path('edit_sdados/<int:pk>', views.edit_sdados, name="edit_sdados"),
    path('criar_terminacao/<int:pk>', views.criar_terminacao, name="criar_terminacao"),
] """
from django.urls import path
from . import views

urlpatterns = [
    path('lista_sdados', views.sdados_list, name='sdados_list'),
    path('disabled/', views.sdados_disabled, name='sdados_disabled'),
    path('sdados/<int:pk>/', views.sdados_detail, name='sdados_detail'),
    path('sdados/<int:pk>/edit/', views.sdados_edit, name='sdados_edit'),
    path('sdados/<int:pk>/disable/', views.sdados_disable, name='sdados_disable'),
    path('sdados/<int:pk>/reactivate/', views.sdados_reactivate, name='sdados_reactivate'),
    path('sterm/<int:pk>/create/', views.sterm_create, name='sterm_create'),
    path('sterm/<int:pk>/edit/', views.sterm_edit, name='sterm_edit'),
]