from django.contrib import admin
from .models import Machine, OID, SurveillanceManager, Logs, Graphique

admin.site.register(Machine)
admin.site.register(OID)
admin.site.register(SurveillanceManager)
admin.site.register(Logs)
admin.site.register(Graphique)