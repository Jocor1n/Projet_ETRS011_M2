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

class OID(models.Model):
    name = models.CharField(max_length=255)
    oid = models.CharField(max_length=255)
    
class SurveillanceManager(models.Model):
    idMachine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    information_type = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    data = models.CharField(max_length=255)

class Logs(models.Model):
    date = models.DateTimeField(default=timezone.now)
    idMachine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    type_log = models.CharField(max_length=255)
    informations = models.CharField(max_length=255)
    is_error = models.BooleanField(default=False)
