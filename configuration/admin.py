from django.contrib import admin
from .models import Machine, OID, SurveillanceManager, Logs, Graphique, Machine_has_OID, Graphique_has_Machine

admin.site.register(Machine)
admin.site.register(OID)
admin.site.register(SurveillanceManager)
admin.site.register(Logs)
admin.site.register(Graphique)
admin.site.register(Machine_has_OID)
admin.site.register(Graphique_has_Machine)