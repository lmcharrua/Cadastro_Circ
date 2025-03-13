from django.db import models

# Create your models here.

class circ_Foe(models.Model):
    n_circ = models.CharField(max_length=15, help_text = 'Número/referência de Circuito', verbose_name = 'Número de circuito')
    ref_enc = models.CharField(max_length=20, help_text = 'Referência de encomenda', verbose_name = 'Referência de encomenda', default='')
    cliente = models.TextField(max_length=150, help_text = 'Nome do cliente',verbose_name = 'Cliente' , default='')
    dist_km = models.DecimalField(max_digits=6, decimal_places=3, help_text = 'Distância km', verbose_name = 'Distância km', default=0)
    dist_optica = models.DecimalField(max_digits=6, decimal_places=3, help_text = 'Distância Óptica', verbose_name = 'Distância Óptica', default=0)
    data_entrega = models.DateField(auto_now=False, auto_now_add=False, help_text = 'Data de entrega', verbose_name = 'Data de     entrega', default='0000-00-00')
    data_ocupa = models.DateField(auto_now=False, auto_now_add=False, help_text = 'Data de ocupação', verbose_name = 'Data de ocupação', default='0000-00-00')
    estado = models.TextField(max_length=20, help_text = 'Estado do circuito', verbose_name = 'Estado do circuito', default='Inst')
    local_a = models.TextField(max_length=150, help_text = 'Local A', verbose_name = 'Local A', default='')
    ligacao_a = models.TextField(max_length=20, help_text = 'Ligação local A', verbose_name = 'Ligação local A', default='')
    local_b = models.TextField(max_length=150, help_text = 'Local B', verbose_name = 'Local B', default='')
    ligacao_b = models.TextField(max_length=20, help_text = 'Ligação local B', verbose_name = 'Ligação local B', default='')
    observacoes = models.TextField(max_length=150, help_text = 'Observações', verbose_name = 'Observações', default='')

    
    class Meta:
        ordering = ['n_circ']
    
    def __str__(self):
        return circ_Foe.n_circ
    