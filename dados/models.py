from django.db import models

# Create your models here.
class serv_dados(models.Model):
    ISID = models.CharField(max_length=10, unique=True)  # Allow blank=True
    ISID_name = models.CharField(max_length=100)
    Service_type = models.CharField(max_length=100)
    Mux_mode = models.CharField(max_length=100)     # Allow blank=True
    Service_status = models.CharField(max_length=100)   # Allow blank=True
    Connect_type = models.CharField(max_length=100) # Allow blank=True
    VLAN_translation = models.CharField(max_length=100) # Allow blank=True
    Cliente = models.CharField(max_length=100) 
    Notas = models.CharField(max_length=100, blank=True)    # Allow blank=True
    class Meta:
        ordering = ['ISID']

    def __str__(self):
        return self.ISID_name

class terminacao(models.Model):
    main_isid = models.ForeignKey('serv_dados', on_delete=models.CASCADE)
    Local = models.CharField(max_length=100)
    Morada = models.CharField(max_length=100)   # Allow blank=True
    Cod_Postal = models.CharField(max_length=100) # Allow blank=True
    dicofre = models.CharField(max_length=6)    # Allow blank=True
    Equipamento = models.CharField(max_length=100)
    SAP = models.CharField(max_length=100)
    Notas = models.CharField(max_length=100, blank=True)    # Allow blank=True

    class Meta:
        ordering = ['main_isid']
    
    def __str__(self):
        return self.Local
    