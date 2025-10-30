

from django.urls import path
from . import views
#from .views import downteste

urlpatterns = [
    path('lista_cct',views.lista_cct, name="lista_cct"),
    path('editar_circuito/<int:pk>', views.editar_circuito, name='editar_circuito'),
    path('criar_circuito', views.criar_circuito, name='criar_circuito'),
    path('download', views.download, name='download'),
]
