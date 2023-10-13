from django.contrib import admin
from .models import Machine, Utilisateur, OID, SurveillanceManager, Graphique, Logs

admin.site.register(Machine)
admin.site.register(Utilisateur)
admin.site.register(OID)
admin.site.register(SurveillanceManager)
admin.site.register(Graphique)
admin.site.register(Logs)