from .models import Machine, OID, SurveillanceManager, Logs, Graphique, Machine_has_OID, Graphique_has_Machine
from .forms import MachineForm, UtilisateurForm, OIDForm, GraphiqueForm, GetMachineForm, MachinehasOIDForm, GraphiquehasMachineForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings 
import os
from django.http import HttpResponse
import math

@login_required
def index(request):
    return render(request, 'index.html')

""" CRUD MACHINE """

@login_required
def add_machine(request):
    form = MachineForm()  # Initialiser le formulaire pour les requêtes GET

    if request.method == 'POST' and 'add_machine' in request.POST:
        form = MachineForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect("liste_machines")

    return render(request, 'add_configuration.html', {'form': form})

@login_required
def liste_machines(request):
    machines = Machine.objects.all()
    return render(request, 'liste_machines.html', {'machines': machines})

@login_required
def edit_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    if request.method == 'POST':
        form = MachineForm(request.POST, instance=machine)
        if form.is_valid():
            form.save()
            return redirect('liste_machines')
    else:
        form = MachineForm(instance=machine)
    return render(request, 'edit_machine.html', {'form': form})

@login_required
def delete_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    if request.method == 'POST':
        machine.delete()
        return redirect('liste_machines')
    return render(request, 'confirm_delete_machines.html', {'object': machine})

""" CRUD UTILISATEUR """

@login_required
def add_user(request):
    form = UtilisateurForm()

    if request.method == 'POST' and 'add_user' in request.POST:
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['mail']  # Note: User model utilise 'email' plutôt que 'mail'
            is_admin = form.cleaned_data['is_admin']

            # Utilisez create_user pour le hachage correct du mot de passe
            user = User.objects.create_user(username=username, password=password, email=email, 
                                            first_name=first_name, last_name=last_name)
            
            if is_admin:
                user.is_superuser = True
                user.is_staff = True
                user.save()
            else: 
                user.is_superuser = False
                user.is_staff = False
                user.save()
                

            return redirect("liste_users")
        else:
            print(form.errors)

    return render(request, 'add_utilisateur.html', {'form': form})

@login_required
def liste_users(request):
    users = User.objects.all()
    return render(request, 'liste_users.html', {'users': users})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('liste_users')
    return render(request, 'confirm_delete_users.html', {'object': user})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['login']
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['mail'] 
                        
            if form.cleaned_data['password'] != ""   :
                user.set_password(form.cleaned_data['password'])
            
            is_admin = form.cleaned_data['is_admin']
            
            if is_admin:
                user.is_superuser = True
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = False
            
            user.save()
        
            return redirect('liste_users')
    else:
        form = UtilisateurForm(initial={
    'login': user.username,
    'last_name': user.last_name,
    'first_name': user.first_name,
    'is_admin': user.is_superuser,
    'mail': user.email
})
    
    return render(request, 'edit_user.html', {'form': form})

""" CRUD OIDS """

@login_required
def add_oid(request):
    form = OIDForm()  # Initialiser le formulaire pour les requêtes GET

    if request.method == 'POST' and 'add_oid' in request.POST:
        form = OIDForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect("liste_oids")
        else:
            print(form.errors)

    return render(request, 'add_oid.html', {'form': form})

@login_required
def liste_oids(request):
    oids = OID.objects.all()
    machines_oids = Machine_has_OID.objects.all()
    
    dictionary = {}
    for oid in oids :
        dictionary.update({oid: list(Machine_has_OID.objects.all().filter(OID=oid))})
    
    return render(request, 'liste_oids.html', {'oids': oids, 'dictionary': dictionary, 'machines_oids':machines_oids})

@login_required
def edit_oid(request, oid_id):
    oid = get_object_or_404(OID, id=oid_id)
    if request.method == 'POST':
        form = OIDForm(request.POST , instance=oid)
        if form.is_valid():
            form.save()
            return redirect('liste_oids')
    else:
        form = OIDForm(instance=oid)
    
    return render(request, 'edit_oid.html', {'form': form})


@login_required
def delete_oid(request, oid_id):
    oid = get_object_or_404(OID, id=oid_id)
    if request.method == 'POST':
        oid.delete()
        return redirect('liste_oids')
    return render(request, 'confirm_delete_oids.html', {'object': oid})

""" ADD and DELETE Machine_has_OID"""

@login_required
def add_machine_has_OID(request, key):
    OID_machine = OID.objects.get(name=key)  

    if request.method == 'POST' and 'add_machine_oid' in request.POST:
        form = MachinehasOIDForm(request.POST)  
        if form.is_valid():
            machine_value = form.cleaned_data['machine']
            oid_value = form.cleaned_data['OID']
            if not Machine_has_OID.objects.filter(OID=oid_value, machine=machine_value).exists() :
                form.save()
            return redirect("liste_oids")
        else:
            print(form.errors)
    else: 
        form = MachinehasOIDForm(initial={'OID': OID_machine})

    return render(request, 'add_machine_oid.html', {'form': form, 'OID_machine': OID_machine})


@login_required
def delete_machine_has_OID(request, machine_oid_id):
    machine_oid = get_object_or_404(Machine_has_OID, id=machine_oid_id)
    if request.method == 'POST':
        machine_oid.delete()
        return redirect('liste_oids')
    return render(request, 'confirm_delete_machine_oid.html', {'object': machine_oid})

""" ADD, EDIT and DELETE Graphique_has_Machine"""

@login_required
def add_graphique_has_machine(request, key):
    graphique_machine = get_object_or_404(Graphique, id=key)

    if request.method == 'POST' and 'add_graphique_machine' in request.POST:
        form = GraphiquehasMachineForm(request.POST, graphique=graphique_machine)  
        if form.is_valid():
            machine_value = form.cleaned_data['machine']
            graphique_value = form.cleaned_data['graphique']
            if not Graphique_has_Machine.objects.filter(graphique=graphique_value, machine=machine_value).exists() :
                form.save()
            return redirect("liste_graphiques")
        else:
            print(form.errors)
    else: 
        form = GraphiquehasMachineForm(graphique=graphique_machine)

    return render(request, 'add_graphique_machine.html', {'form': form, 'graphique_machine': graphique_machine})


@login_required
def delete_graphique_has_machine(request, graphique_machine_id):
    graphique_machine = get_object_or_404(Graphique_has_Machine, id=graphique_machine_id)
    if request.method == 'POST':
        graphique_machine.delete()
        return redirect('liste_graphiques')
    return render(request, 'confirm_delete_graphique_machine.html', {'object': graphique_machine})


@login_required
def edit_graphique_machine(request, graphique_machine_id):
    graphique_machine = get_object_or_404(Graphique_has_Machine, id=graphique_machine_id)
    graphique_instance = graphique_machine.graphique

    if request.method == 'POST':
        form = GraphiquehasMachineForm(request.POST, instance=graphique_machine, graphique=graphique_instance)
        if form.is_valid():
            form.save()
            return redirect('liste_graphiques')
    else:
        form = GraphiquehasMachineForm(instance=graphique_machine, graphique=graphique_instance)
    
    return render(request, 'edit_graphique_machine.html', {'form': form})



""" CRUD Graphiques """

@login_required
def add_graphique(request):
    form = GraphiqueForm()  # Initialiser le formulaire pour les requêtes GET

    if request.method == 'POST' and 'add_graphique' in request.POST:
        form = GraphiqueForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect("liste_graphiques")
        else:
            print(form.errors)

    return render(request, 'add_graphique.html', {'form': form})

@login_required
def liste_graphiques(request):
    graphiques = Graphique.objects.all()
    machines = Machine.objects.all()
    
    dictionary_machines = {}
    for machine in machines :
        dictionary_machines.update({machine: list(Graphique_has_Machine.objects.all().filter(machine=machine).order_by('ordre'))})
    
    dictionary_graphiques = {}
    for graphique in graphiques :
        dictionary_graphiques.update({graphique: list(Graphique_has_Machine.objects.all().filter(graphique=graphique))})
    
    return render(request, 'liste_graphiques.html', {'graphiques': graphiques, 'dictionary_machines': dictionary_machines, 'dictionary_graphiques':dictionary_graphiques})

@login_required
def edit_graphique(request, graphique_id):
    graphique = get_object_or_404(Graphique, id=graphique_id)
    if request.method == 'POST':
        form = GraphiqueForm(request.POST, instance=graphique )
        if form.is_valid():
            form.save()
            return redirect('liste_graphiques')
        else:
            print(form.errors)
    else:
        form = GraphiqueForm(instance=graphique)
    
    return render(request, 'edit_graphique.html', {'form': form})

@login_required
def delete_graphique(request, graphique_id):
    graphique = get_object_or_404(Graphique, id=graphique_id)
    if request.method == 'POST':
        graphique.delete()
        return redirect('liste_graphiques')
    return render(request, 'confirm_delete_graphique.html', {'object': graphique})


@login_required
def donnees_machines(request):
    machines = Machine.objects.all()
    # graphiques = Graphique.objects.all().order_by("ordre")
    
    machine = machines[0]

    if request.method == 'POST':
        form = GetMachineForm(request.POST)
        if form.is_valid():
            machine_select = form.cleaned_data['name']
            machine = Machine.objects.all().get(name=machine_select)
    else:
        form = GetMachineForm()
    
    # Récupération des graphiques liés à la machine sélectionnée
    graphiques_machines = Graphique_has_Machine.objects.filter(machine=machine).order_by('ordre')
    graphiques = [gm.graphique for gm in graphiques_machines]

    data = {
        'name': machine,
        'types': {},
    }

    # Votre traitement des informations reste inchangé
    information_types = SurveillanceManager.objects.filter(idMachine=machine).values_list('information_type', flat=True).distinct()
    for info_type in information_types:
        if OID.objects.get(name=info_type).Donnee_fixe == False:
            data['types'][info_type] = SurveillanceManager.objects.filter(idMachine=machine, information_type=info_type)
        else:
            data['types'][info_type] = SurveillanceManager.objects.filter(idMachine=machine, information_type=info_type).latest("date")

    data_graphiques = []   
    
    
    def format_hours(hours):
        return f"{hours}h 0min 0secondes"
    
    def format_minutes(minutes):
        minutes = int(minutes)
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}h {minutes}min 0secondes"
    
    def format_seconds(seconds):
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours}h {minutes}min {seconds}secondes"
    
    def cent_format_seconds(cent_seconds):
        seconds = int(cent_seconds) // 100
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours}h {minutes}min {seconds}secondes"
    
    def ratio_to_pourcentage(ratio):
        return math.ceil(float(ratio) * 100)
    
    def pourcentage_to_ratio(pourcentage):
        return math.ceil(float(pourcentage) / 100)
    
    def boulean_to_text(boolean):
        if int(boolean) == 1 :
            return "Vrai"
        else:
            return "Faux"
        
    def do_conversion(graphique_entree, graphique_sortie, to_convert):
        if graphique_entree == "Heure":
            to_convert = format_hours(to_convert)
        
        elif graphique_entree == "Minute":
            to_convert = format_minutes(to_convert)
            
        elif graphique_entree == "Seconde":
            to_convert = format_seconds(to_convert)
            
        elif graphique_entree == "CentSeconde":
            to_convert = cent_format_seconds(to_convert)
                     
        elif graphique_entree == "Ratio" and graphique_sortie == "Pourcentage":
            to_convert = ratio_to_pourcentage(to_convert)
    
        elif graphique_entree == "Pourcentage" and graphique_sortie == "Ratio":
            to_convert = pourcentage_to_ratio(to_convert)
            
        elif graphique_entree == "Boolean" and graphique_sortie == "Texte":
            to_convert = boulean_to_text(to_convert)
            
        return to_convert
    
    for graphique in graphiques :
        list_temp = []
        if graphique.GraphiqueType == "Texte":
            list_temp.append("Texte")
            list_temp.append(graphique)
           
            if graphique.type_de_donnees_entree == graphique.type_de_donnees_sortie:
                list_temp.append(data["types"][graphique.OID1.name].data)
            else:
                to_convert = data["types"][graphique.OID1.name].data    
                convert = do_conversion(graphique.type_de_donnees_entree, graphique.type_de_donnees_sortie, to_convert)      
                list_temp.append(convert)
           
        elif graphique.GraphiqueType == "Curseur":
            list_temp.append("Curseur")
            list_temp.append(graphique)
            
            if graphique.type_de_donnees_entree == graphique.type_de_donnees_sortie:
                list_temp.append(data["types"][graphique.OID1.name].data)
            else:
                to_convert = data["types"][graphique.OID1.name].data
                convert = do_conversion(graphique.type_de_donnees_entree, graphique.type_de_donnees_sortie, to_convert)
                list_temp.append(convert)
                
                
        else :
            list_temp.append("Fleche")
            list_temp.append(graphique)
            liste_queryset = []
            liste_groupe = []
            for element in list(data["types"][graphique.OID1.name]):
                liste_groupe.append(element)       
                if graphique.type_de_donnees_entree == graphique.type_de_donnees_sortie:
                    liste_groupe.append(element.data)
                    liste_queryset.append(liste_groupe)
                    liste_groupe = []
                else:
                    to_convert =element.data
                    
                    convert = do_conversion(graphique.type_de_donnees_entree, graphique.type_de_donnees_sortie, to_convert)
                                            
                    liste_groupe.append(convert)
                    liste_queryset.append(liste_groupe)
                    liste_groupe = []
                
            list_temp.append(liste_queryset)
            
            liste_queryset2 = []
            try:
                
                if data["types"][graphique.OID2.name] != None:
                    for element in list(data["types"][graphique.OID2.name]):
                        liste_groupe.append(element)       
                        if graphique.type_de_donnees_entree == graphique.type_de_donnees_sortie:
                            liste_groupe.append(element.data)
                            liste_queryset2.append(liste_groupe)
                            liste_groupe = []
                        else:
                            to_convert =element.data
                            
                            convert = do_conversion(graphique.type_de_donnees_entree, graphique.type_de_donnees_sortie, to_convert)
                                                    
                            liste_groupe.append(convert)
                            liste_queryset2.append(liste_groupe)
                            liste_groupe = []
            except AttributeError:
                liste_queryset2.append(["",""])
            list_temp.append(liste_queryset2)
            
        data_graphiques.append(list_temp)
        
    return render(request, 'liste_donnees.html', {'data_graphiques': data_graphiques, 'machines' : machines, 'form': form})


@login_required
def logs(request):
    logs = Logs.objects.all()
    return render(request, 'liste_logs.html', {'logs': logs})

def download_log(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'log/debug7.log')

    # Assurez-vous que le fichier existe
    if os.path.exists(log_file_path):
        with open(log_file_path, 'rb') as log_file:
            response = HttpResponse(log_file.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename="debug7.log"'
            return response
    else:
        return HttpResponse("Désolé, le fichier log n'a pas été trouvé", status=404)