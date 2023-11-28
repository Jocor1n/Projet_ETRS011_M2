from django import forms
from .models import Machine, Graphique, OID, Machine_has_OID, Graphique_has_Machine
from django.db.models import Q


class MachineForm (forms.ModelForm):
    class Meta :
        model = Machine
        fields = ['name' , 'IPAdresse', 'SNMPType', 'Community']
                               
class UtilisateurForm (forms.Form):
    login = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, required=False)  
    last_name = forms.CharField(max_length=255, required=False)
    first_name = forms.CharField(max_length=255, required=False)
    TRUE_FALSE_CHOICES = (
    (True, 'Oui'),
    (False, 'Non')
    )
    is_admin = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, widget=forms.RadioSelect)
    mail = forms.EmailField(max_length=255)
    
    def clean_is_admin(self):
        # Convertit la valeur soumise en booléen
        is_admin_value = self.cleaned_data['is_admin']
        return is_admin_value == 'True'
                               
class OIDForm (forms.ModelForm):
    class Meta :
        model = OID
        fields = ['name' , 'oid', 'Donnee_fixe']
    
class GraphiqueForm (forms.ModelForm):
    class Meta :
        model = Graphique
        fields = ['name', 'GraphiqueType', 'axex', 'axey', 'OID1', 'OID2', 'valeur_max','type_de_donnees_entree','type_de_donnees_sortie']
        
class GetMachineForm (forms.Form):
    name = forms.CharField(max_length=255)


class MachinehasOIDForm(forms.ModelForm):
    class Meta :
        model = Machine_has_OID
        fields = ['machine', 'OID']

class GraphiquehasMachineForm(forms.ModelForm):
    class Meta :
        model = Graphique_has_Machine
        fields = ['graphique', 'machine', 'ordre']

    def __init__(self, *args, **kwargs):
        graphique_instance = kwargs.pop('graphique', None)
        super(GraphiquehasMachineForm, self).__init__(*args, **kwargs)
        if graphique_instance:
            self.fields['machine'].queryset = self.get_filtered_machines(graphique_instance)

    def get_filtered_machines(self, graphique):
        oid1 = graphique.OID1
        oid2 = graphique.OID2
    
        # Requête initiale pour les machines avec OID1
        machines_with_oid1_query = Machine_has_OID.objects.filter(OID=oid1).values_list('machine', flat=True)
    
        # Filtrer ces machines pour obtenir celles qui ont également OID2
        if oid2:
            machines_with_oid2_query = Machine_has_OID.objects.filter(OID=oid2).values_list('machine', flat=True)
            # Utilisation de l'intersection des deux sets pour obtenir les machines qui sont dans les deux listes
            machine_ids = set(machines_with_oid1_query).intersection(set(machines_with_oid2_query))
        else:
            machine_ids = set(machines_with_oid1_query)
    
        # Obtenir les machines correspondantes
        machines = Machine.objects.filter(id__in=machine_ids)
        return machines



