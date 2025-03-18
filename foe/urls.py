from django.urls import path
from . import views

urlpatterns = [
    path('lista_foe',views.lista_foe, name="lista_foe"),
    path('editar_foe/<int:pk>', views.editar_foe, name='editar_foe'),
    path('criar_foe', views.criar_foe, name='criar_foe'),
    path('desligados_foe',views.desligados_foe, name="desligados_foe"),
]