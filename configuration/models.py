from django.db import models

class Utilisateur(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    mail = models.EmailField()

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

class OID(models.Model):
    oid = models.CharField(max_length=255)
    
class SurveillanceManager(models.Model):
    idMachine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    information_type = models.CharField(max_length=255)
    data = models.CharField(max_length=255)

class Graphique(models.Model):
    idSurveillance = models.ForeignKey(SurveillanceManager, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    x_label = models.CharField(max_length=255)
    y_label = models.CharField(max_length=255)
    x_info = models.CharField(max_length=255)
    y_info = models.CharField(max_length=255)

class Logs(models.Model):
    idMachine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    informations = models.CharField(max_length=255)
    is_error = models.BooleanField(default=False)
