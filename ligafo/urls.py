from django.urls import path
from . import views

urlpatterns = [
    path('lista_ligafo',views.lista_ligafo, name="lista_ligafo"),
    path('editar_ligafo/<int:pk>', views.editar_ligafo, name='editar_ligafo'),
    path('criar_ligafo', views.criar_ligafo, name='criar_fo'),
]