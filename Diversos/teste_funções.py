from django.db import models
from django.db.models import Max
from django.utils.functional import cached_property

class Circuit(models.Model):
    n_circuito = models.CharField(max_length=9, unique=True, editable=False)
    # Add other fields as needed
    def save(self, *args, **kwargs):
            if not self.n_circuito:
                self.n_circuito = self.generate_n_circuito()
            super().save(*args, **kwargs)
    @classmethod
    def generate_n_circuito(cls):
        prefix = "RFT"
        last_circuit = cls.objects.aggregate(max_n_circuito=Max('n_circuito'))['max_n_circuito']
        if last_circuit:
            last_number = int(last_circuit.replace(prefix, ""))
            new_number = last_number + 1
        else:
            new_number = 1
        return f"{prefix}{new_number:06d}"
