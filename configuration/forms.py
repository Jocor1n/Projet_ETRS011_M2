from django import forms
from .models import Machine, Graphique, OID

class MachineForm (forms.ModelForm):
    class Meta :
        model = Machine
        fields = ['name' , 'IPAdresse', 'SNMPType', 'Community']
                               
class UtilisateurForm (forms.ModelForm):
    login = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)  
    last_name = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    TRUE_FALSE_CHOICES = (
    (True, 'Oui'),
    (False, 'Non')
    )
    is_admin = forms.ChoiceField(choices=TRUE_FALSE_CHOICES)
    mail = forms.EmailField(max_length=255)
                               
class OIDForm (forms.ModelForm):
    class Meta :
        model = OID
        fields = ['name' , 'oid', 'is_Integer', 'Donnee_fixe']
    
class GraphiqueForm (forms.ModelForm):
    class Meta :
        model = Graphique
        fields = ['name', 'GraphiqueType', 'axex', 'axey', 'ordre', 'OID1', 'OID2', 'valeur_max']
        
class GetMachineForm (forms.Form):
    name = forms.CharField(max_length=255)


