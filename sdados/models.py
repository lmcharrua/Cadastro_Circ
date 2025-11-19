from django.db import models
import datetime
from django.utils import timezone


class sdados(models.Model):
    isid = models.CharField(max_length=10, unique=True)  # Allow blank=True
    isid_name = models.CharField(max_length=100)
    estado = models.CharField(max_length=3, default='A')
    service_type = models.CharField(max_length=100)
    mux_mode = models.CharField(max_length=100, blank=True)     # Allow blank=True
    connect_type = models.CharField(max_length=100, blank=True) # Allow blank=True
    vlan_translation = models.CharField(max_length=100, blank=True) # Allow blank=True
    cliente = models.CharField(max_length=100) 
    notas = models.CharField(max_length=100, blank=True, default='')    # Allow blank=True
    created_at = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, default=datetime.date.today)
    class Meta:
        ordering = ['isid']

    def __str__(self):
        return self.isid_name

class sterm(models.Model):
    misid = models.CharField(max_length=10)  # Foreign key to sdados, should match ISID
    local = models.CharField(max_length=100)
    morada = models.CharField(max_length=100, blank=True, default= '')   # Allow blank=True
    cod_postal = models.CharField(max_length=100, blank=True, default=''   ) # Allow blank=True
    equipamento = models.CharField(max_length=100)
    sap = models.CharField(max_length=100)
    estado = models.CharField(max_length=3, default='A')
    data_actualizacao = models.DateField(null=True, blank=True)
    notas = models.CharField(max_length=100, blank=True)    # Allow blank=True

    class Meta:
        ordering = ['sap']
    
    def __str__(self):
        return self.local
