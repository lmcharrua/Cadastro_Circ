from django.db import models

# Create your models here.
class circfoe(models.Model):
    referencia = models.CharField(max_length=20, verbose_name='Referência', null=True, help_text='Referência')
    encomenda = models.CharField(max_length=20, default="ref encomenda", verbose_name='Encomenda', help_text='Encomenda')
    cliente = models.CharField(max_length=30, blank=True, null=True, verbose_name='Cliente', help_text='Cliente')
    dist_km = models.DecimalField(max_digits=6, decimal_places=3, default="000.000", verbose_name='Distância Kilométrica', help_text='Distância km IET50')
    dist_optica = models.DecimalField(max_digits=6, decimal_places=3, default="000.000", verbose_name='Distância km ótica', help_text='Distância km ótica')
    data_obj = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Data objectivo', help_text='Data objectivo')
    data_entrega = models.DateField(auto_now=False, auto_now_add=False, default="2025-12-31", verbose_name='Data entrega', help_text='Data entrega')
    data_ocupa = models.DateField(auto_now=False, auto_now_add=False, default="2025-12-31", verbose_name='Data ocupação', help_text='Data ocupação')
    tipo_ocupa = models.CharField(max_length=20, verbose_name='Tipo Ocupação', help_text='Tipo Ocupação', null=True)
    estado = models.CharField(max_length=20, verbose_name='Estado', default="I", help_text='Estado')
    local_a = models.CharField(max_length=150, verbose_name='Local A', default="Local A", help_text='Local A')
    ligacao_a = models.CharField(max_length=20, null=True)
    local_b = models.CharField(max_length=150, verbose_name='Local B',default="Local B",  help_text='Local B')
    ligacao_b = models.CharField(max_length=20, null=True)
    observacoes = models.TextField(max_length=150, verbose_name='Observações', help_text='Observações', null=True)

    class Meta:
        ordering = ['referencia']

    def __str__(self):
        return self.referencia