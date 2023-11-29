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
        ('Texte', 'Texte')
    ]
    GraphiqueType = models.CharField(max_length=255,choices=Graphique_Types, default='1')
    axex = models.CharField(max_length=255, blank=True, null=True)
    axey = models.CharField(max_length=255, blank=True, null=True)
    OID1 = models.ForeignKey(OID, on_delete=models.CASCADE, related_name='OID1')
    OID2 = models.ForeignKey(OID, on_delete=models.CASCADE, related_name='OID2', blank=True, null=True)
    valeur_max = models.IntegerField(default=0)
    Donnees_Types = [
        ('Texte', 'Texte'), 
        ('Entier', 'Entier'), 
        ('Boolean', 'Boolean'),    
        ('Heure', 'Heure'),
        ('Minute', 'Minute'),
        ('Seconde', 'Seconde'),
        ('CentSeconde', 'CentSeconde'),
        ('Ratio', 'Ratio'),
        ('Pourcentage', 'Pourcentage')
    ]
    type_de_donnees_entree = models.CharField(max_length=255,choices=Donnees_Types, default='Texte')
    type_de_donnees_sortie = models.CharField(max_length=255,choices=Donnees_Types, default='Texte')
    def __str__(self):
        return self.name

class Machine_has_OID(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    OID = models.ForeignKey(OID, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.machine.name + " " +  self.OID.name

class Graphique_has_Machine(models.Model):
    graphique = models.ForeignKey(Graphique, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    ordre = models.IntegerField(default=1)
    
    def __str__(self):
        return self.graphique.name + " "+ self.machine.name
    

