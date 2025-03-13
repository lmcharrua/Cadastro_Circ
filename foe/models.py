from django.db import models

# Create your models here.

class Foe(models.Model):
    n_circ = models.CharField(max_length=20, help_text = 'Número/referência de Circuito', verbose_name = 'Número de circuito')
    cliente = models.TextField(max_length=150, help_text = 'Nome do cliente',verbose_name = 'Cliente' , default='')
    dist_iet = models.DecimalField(max_digits=6, decimal_places=3, help_text = 'Distância IET50', verbose_name = 'Distância IET50', default=0)
    dist_optica = models.DecimalField(max_digits=6, decimal_places=3, help_text = 'Distância Óptica', verbose_name = 'Distância Óptica', default=0)
    data_pedido = models.DateField(auto_now=False, auto_now_add=False, help_text = 'Data do pedido', verbose_name = 'Data do pedido')
    data_entrega = models.DateField(auto_now=False, auto_now_add=False, help_text = 'Data de entrega', verbose_name = 'Data de entrega')
    estado = models.TextField(max_length=20, help_text = 'Estado do circuito', verbose_name = 'Estado do circuito', default='Inst')
    local_a = models.TextField(max_length=150, help_text = 'Local A', verbose_name = 'Local A', default='')
    equip_a = models.TextField(max_length=20, help_text = 'Equipamento local A', verbose_name = 'Equipamento local A', default='')
    slot_a = models.CharField(max_length=15, help_text = 'Slot local A', verbose_name = 'Slot local A', default='---')
    porta_a = models.CharField(max_length=15, help_text = 'Porta local A', verbose_name = 'Porta local A', default='---')
    local_b = models.TextField(max_length=150, help_text = 'Local B', verbose_name = 'Local B', default='')
    equip_b = models.TextField(max_length=20, help_text = 'Equipamento local B', verbose_name = 'Equipamento local B', default='')
    slot_b = models.CharField(max_length=15, help_text = 'Slot local B', verbose_name = 'Slot local B', default='---')
    porta_b = models.CharField(max_length=15, help_text = 'Porta local B', verbose_name = 'Porta local B', default='---')
    observacoes = models.TextField(max_length=150, help_text = 'Observações', verbose_name = 'Observações', default='')

    
    class Meta:
        ordering = ['n_circ']
    
    def __str__(self):
        return Foe.n_circ
    