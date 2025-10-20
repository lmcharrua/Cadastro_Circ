from django.db import models
import datetime
from functools import reduce
from django.db.models import Max
from django.utils.functional import cached_property

class Cartas(models.Model):
    fabricante = models.CharField(max_length=50, help_text='Nome do fabricante da carta', verbose_name='Fabricante')
    data_rececao = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, default=datetime.date.today, help_text='Data de receção da carta', verbose_name='Data de receção')
    b_type = models.CharField(max_length=20, help_text='Tipo de carta', verbose_name='Tipo de carta')
    part_number = models.CharField(max_length=20, help_text='Model number', verbose_name='Model number')
    serial_number = models.CharField(max_length=20, help_text='Número de série da carta', verbose_name='Número de série')
    descricao = models.CharField(max_length=50, help_text='Descrição da carta', null=True, blank=True, verbose_name='Descrição')
    estado = models.CharField(max_length=5, help_text='Estado da carta', verbose_name='Estado')
    projeto = models.CharField(max_length=50, help_text='Projeto associado à carta', null=True, blank=True, verbose_name='Projeto')
    sistema = models.CharField(max_length=50, help_text='Sistema associado à carta', null=True, blank=True, verbose_name='Sistema')
    localizacao = models.CharField(max_length=100, help_text='Localização física da carta', null=True, blank=True, verbose_name='Localização') 
    equipamento = models.CharField(max_length=20, help_text='Equipamento onde a carta está instalada', null=True, blank=True, verbose_name='Equipamento')
    subrack = models.CharField(max_length=10, help_text='Subrack onde a carta está instalada', null=True, blank=True, verbose_name='Subrack')
    slot = models.CharField(max_length=2, help_text='Slot onde a carta está instalada', null=True, blank=True, verbose_name='Slot')
    porto = models.CharField(max_length=2, help_text='Porto onde a carta está instalada', null=True, blank=True, verbose_name='Porto')
    observacoes = models.TextField(max_length=200, help_text='Observações adicionais', verbose_name='Observações', blank=True)

    class Meta:
        ordering = ['fabricante', 'part_number', 'serial_number']

    def __str__(self):
        return f"{self.fabricante} - {self.part_number} - {self.serial_number}"
    

class hist_cartas(models.Model):
    carta = models.ForeignKey(Cartas, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    utilizador = models.CharField(max_length=50)

    class Meta:
        ordering = ['-data_alteracao']

    def __str__(self):
        return f"Alteração em {self.carta} por {self.utilizador} em {self.data_alteracao}"