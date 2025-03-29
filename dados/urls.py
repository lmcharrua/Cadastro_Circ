from django.urls import path
from . import views

urlpatterns = [
    path('lista_dados',views.lista_dados, name="lista_dados"),
    path('editar_dados/<int:pk>', views.editar_dados, name='editar_dados'),
    path('criar_dados', views.criar_dados, name='criar_dados'),

]