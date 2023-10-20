from django import forms
from .models import Machine


class MachineForm (forms.Form):
    name = forms.CharField(max_length=255)
    IP = forms.GenericIPAddressField()
    TypeSNMP = forms.ChoiceField(choices=Machine.SNMP_CHOICES)
    Community = forms.CharField(max_length=255)
                               
class UtilisateurForm (forms.Form):
    login = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)  
    last_name = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
    )
    is_admin = forms.ChoiceField(choices=TRUE_FALSE_CHOICES)
    mail = forms.EmailField(max_length=255)
                               