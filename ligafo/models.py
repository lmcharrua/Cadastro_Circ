from django.db import models

# Create your models here.
class ligafo(models.Model):
    referencia = models.CharField(max_length=20, blank=True, null=True, verbose_name='Referência', help_text='Referência')
    cliente = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cliente', help_text='Cliente')
    dist_iet = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Distância km IET50', help_text='Distância km IET50')
    dist_optica = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Distância km ótica', help_text='Distância km ótica')
    data_pedido = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Data pedido', help_text='Data pedido')
    data_entrega = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Data Entrega', help_text='Data Entrega')
    estado = models.CharField(max_length=20, blank=True, null=True, verbose_name='Estado', help_text='Estado')
    local_a = models.CharField(max_length=150, blank=True, null=True, verbose_name='Local A', help_text='Local A')
    equipa_a = models.CharField(max_length=20, blank=True, null=True, verbose_name='Equipamento A', help_text='Equipamento A')
    slot_a = models.CharField(max_length=20, blank=True, null=True, verbose_name='Slot A', help_text='Slot A')
    porta_a = models.CharField(max_length=20, blank=True, null=True, verbose_name='Porta A', help_text='Porta A')
    local_b = models.CharField(max_length=150, blank=True, null=True, verbose_name='Local B', help_text='Local B')
    equipa_b = models.CharField(max_length=20, blank=True, null=True, verbose_name='Equipamento B', help_text='Equipamento B')
    slot_b = models.CharField(max_length=20, blank=True, null=True, verbose_name='Slot B', help_text='Slot B')
    porta_b = models.CharField(max_length=20, blank=True, null=True, verbose_name='Porta B', help_text='Porta B')
    observacoes = models.TextField(max_length=150, blank=True, null=True, verbose_name='Observações', help_text='Observações')

    class Meta:
        ordering = ['referencia']

    def __str__(self):
        return self.referencia
