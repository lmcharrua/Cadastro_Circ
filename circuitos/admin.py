from django.contrib import admin
from .models import Circuitos, Hist_Cct
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(Circuitos) #, SimpleHistoryAdmin)
admin.site.register(Hist_Cct)
