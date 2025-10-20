from django.contrib import admin
from .models import Cartas, hist_cartas

# Register your models here.
admin.site.register(Cartas)
admin.site.register(hist_cartas)