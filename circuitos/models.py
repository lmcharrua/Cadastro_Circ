from django.db import models
from functools import reduce

# Create your models here.

class Circuitos(models.Model):
    N_Circuito = models.CharField(max_length=20, help_text = 'Numero/referencia de Circuito', verbose_name = 'Número de circuito')
    Data_Rate = models.CharField(max_length=10)
    Data_Inst = models.DateField(auto_now=False, auto_now_add=False)
    Data_Activ = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    Estado_Cct = models.TextField(max_length=150, default='Definido')
    Entidade_PTR1 = models.CharField(max_length=30)
    Morada_PTR1 = models.TextField(max_length=150, default='', blank=True)
    Cod_Post_PTR1 = models.CharField(max_length=50, blank=True)
    Interface_PTR1 = models.CharField(max_length=30, blank=True)
    Equip_PTR1 = models.CharField(max_length=20, blank=True)
    Slot_PTR1 = models.CharField(max_length=5, default='---', blank=True)
    Trib_PTR1 = models.CharField(max_length=10, default='---', blank=True)
    Entidade_PTR2 = models.CharField(max_length=30)
    Morada_PTR2 = models.TextField(max_length=150, default='', blank=True)
    Cod_Post_PTR2 = models.CharField(max_length=50, blank=True)
    Interface_PTR2 = models.CharField(max_length=30, blank=True)
    Equip_PTR2 = models.CharField(max_length=20, blank=True)
    Slot_PTR2 = models.CharField(max_length=5, default='---', blank=True)
    Trib_PTR2 = models.CharField(max_length=10, default='---', blank=True)
    User_Cct = models.TextField(max_length=150, blank=False, null=False)
    Propriedade_Cct = models.TextField(max_length=150, default='', blank=True)
    Outras_Ref = models.TextField(max_length=150, default='', blank=True)
 
    def save(self, *args, **kwargs):
        if not self.N_Circuito:
            self.N_Circuito = self.gera_N_circ()
        super().save(*args, **kwargs)
    
    @classmethod
    def gera_N_circ(circuito):
        prefix="RFT"
        lcirc=list(Circuitos.objects.values_list('N_Circuito', flat = True).filter(N_Circuito__startswith='RFT'))
        res=reduce(lambda acc, x: acc + [x[3:]], lcirc, [])
        res2 = list(map(int, res))
        res3=[x for x in res2 if x <= 200000]
        next=max(res3)+1
        return f"{prefix}{next:06d}"

    class Meta:
        ordering = ['N_Circuito']
    
    def __str__(self):
        return self.N_Circuito


class Hist_Cct(models.Model):
    N_Circuito = models.ForeignKey(Circuitos, on_delete=models.CASCADE)
    Data = models.DateField(auto_now=False, auto_now_add=False)
    Accao = models.TextField
    User = models.CharField(max_length=30)
    class Meta:
        ordering = ['-Data']
    
    def __str__(self):
        return Hist_Cct.N_Circuito
    
