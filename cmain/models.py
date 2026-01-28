from django.db import models
from django.contrib.auth.models import User

class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')
    password = models.CharField(max_length=128)  # stores hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Moradas(models.Model):
    Entidade = models.CharField(max_length=100)
    Nome_curto = models.CharField(max_length=50, blank=True, null=True)
    Morada = models.CharField(max_length=255)
    CodigoPostal = models.CharField(max_length=20)
    Localidade = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    Freguesia = models.CharField(max_length=100, blank=True, null=True)
    Dicofre = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.Entidade} - {self.Morada}, {self.CodigoPostal} {self.Localidade}"

     