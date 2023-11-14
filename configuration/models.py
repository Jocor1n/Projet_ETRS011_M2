from django.db import models
from django.utils import timezone

class Machine(models.Model):
    name = models.CharField(max_length=255)
    IPAdresse = models.GenericIPAddressField()
    port = models.IntegerField(default=161)
    SNMP_CHOICES = [
        ('1', 'Version 1'),
        ('2c', 'Version 2c'),
        ('3', 'Version 3')
    ]
    SNMPType = models.CharField(max_length=3, choices=SNMP_CHOICES, default='1')
    Community = models.CharField(max_length=255, default=None)
    
    def __str__(self):
        return self.name
    
class OID(models.Model):
    name = models.CharField(max_length=255)
    oid = models.CharField(max_length=255)
    is_Integer = models.BooleanField(default=False)
    Donnee_fixe = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class SurveillanceManager(models.Model):
    idMachine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    information_type = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    data = models.CharField(max_length=255)
    
    def __str__(self):
        return self.idMachine.name + " " +self.information_type + " " + str(self.date)

class Logs(models.Model):
    date = models.DateTimeField(default=timezone.now)
    idMachine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    type_log = models.CharField(max_length=255)
    informations = models.CharField(max_length=255)
    is_error = models.BooleanField(default=False)
    
    def __str__(self):
        return self.idMachine.name + " " +self.type_log + " " + str(self.date)
    
class Graphique(models.Model):
    name = models.CharField(max_length=255)
    Graphique_Types = [
        ('Fleche', 'Fleche'),
        ('Curseur', 'Curseur'),
        ('Comparaison', 'Comparaison'),
        ('Texte', 'Texte')
    ]
    GraphiqueType = models.CharField(max_length=255,choices=Graphique_Types, default='1')
    axex = models.CharField(max_length=255, blank=True, null=True)
    axey = models.CharField(max_length=255, blank=True, null=True)
    ordre = models.IntegerField()
    OID1 = models.ForeignKey(OID, on_delete=models.CASCADE, related_name='OID1')
    OID2 = models.ForeignKey(OID, on_delete=models.CASCADE, related_name='OID2', blank=True, null=True)
    valeur_max = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
