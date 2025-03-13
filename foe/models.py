from django.db import models

# Create your models here.

class circ_Foe(models.Model):
    n_circ = models.CharField(max_length=15, help_text = 'Número/referência de Circuito', verbose_name = 'Número de circuito')
    ref_enc = models.CharField(max_length=20, help_text = 'Referência de encomenda', verbose_name = 'Referência de encomenda', default='')
    cliente = models.TextField(max_length=150, help_text = 'Nome do cliente',verbose_name = 'Cliente' , default='')
    dist_km = models.DecimalField(max_digits=6, decimal_places=3, help_text = 'Distância km', verbose_name = 'Distância km', default=0)
    dist_optica = models.DecimalField(max_digits=6, decimal_places=3, help_text = 'Distância Óptica', verbose_name = 'Distância Óptica', default=0)
    data_obj = models.DateField(auto_now=False, auto_now_add=False, help_text = 'Data Objetivo', verbose_name = 'Data Objetivo', null=True, blank=True)
    data_entrega = models.DateField(auto_now=False, auto_now_add=False, help_text = 'Data de entrega', verbose_name = 'Data de entrega', null=True, blank=True)
    data_ocupa = models.DateField(auto_now=False, auto_now_add=False, help_text = 'Data de ocupação', verbose_name = 'Data de ocupação', null=True, blank=True)
    estado = models.TextField(max_length=20, help_text = 'Estado do circuito', verbose_name = 'Estado do circuito', default='Inst')
    local_a = models.TextField(max_length=150, help_text = 'Local A', verbose_name = 'Local A', default='')
    ligacao_a = models.TextField(max_length=20, help_text = 'Ligação local A', verbose_name = 'Ligação local A', default='')
    local_b = models.TextField(max_length=150, help_text = 'Local B', verbose_name = 'Local B', default='')
    ligacao_b = models.TextField(max_length=20, help_text = 'Ligação local B', verbose_name = 'Ligação local B', default='')
    observacoes = models.TextField(max_length=250, help_text = 'Observações', verbose_name = 'Observações', default='')
    notas = models.TextField(max_length=250, help_text = 'Notas', verbose_name = 'Notas', default='')

    
    class Meta:
        ordering = ['n_circ']
    
    def __str__(self):
        return circ_Foe.n_circ
    