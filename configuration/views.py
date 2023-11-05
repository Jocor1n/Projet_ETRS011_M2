from .models import Machine, OID, SurveillanceManager, Graphique, Logs
from .forms import MachineForm, UtilisateurForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings 
import os
import json
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd


@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def add_machine(request):
    form = MachineForm()  # Initialiser le formulaire pour les requêtes GET

    if request.method == 'POST' and 'add_machine' in request.POST:
        form = MachineForm(request.POST)  
        if form.is_valid():
            name = form.cleaned_data['name']
            IP = form.cleaned_data['IP']  
            TypeSNMP = form.cleaned_data['TypeSNMP']  
            Community = form.cleaned_data['Community'] 
            
            Machine.objects.create(name=name, IPAdresse=IP, SNMPType=TypeSNMP, Community=Community)
            return redirect("/")
        else:
            print(form.errors)

    return render(request, 'configuration.html', {'form': form})

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

            return redirect("/")
        else:
            print(form.errors)

    return render(request, 'utilisateur.html', {'form': form})

@login_required
def liste_machines(request):
    machines = Machine.objects.all()
    return render(request, 'liste_machines.html', {'machines': machines})

@login_required
def liste_users(request):
    users = User.objects.all()
    return render(request, 'liste_users.html', {'users': users})

@login_required
def edit_machine(request, machine_id):
    form = MachineForm()
    machine = get_object_or_404(Machine, id=machine_id)
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            machine.name = form.cleaned_data['name']
            machine.IPAdresse = form.cleaned_data['IP']
            machine.SNMPType = form.cleaned_data['TypeSNMP']
            machine.Community = form.cleaned_data['Community']
            machine.save()
            return redirect('liste_machines')
    else:
        form = MachineForm(initial={
        'name': machine.name,
        'IP': machine.IPAdresse,
        'TypeSNMP': machine.SNMPType,
        'Community': machine.Community
        })
    return render(request, 'edit_machine.html', {'form': form})

@login_required
def delete_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    if request.method == 'POST':
        machine.delete()
        return redirect('liste_machines')
    return render(request, 'confirm_delete_machines.html', {'object': machine})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('liste_users')
    return render(request, 'confirm_delete_users.html', {'object': user})

@login_required
def donnees_machines(request):
    machines_data = []
    machines = Machine.objects.all()
    
    for machine in machines:
        data = {
            'name': machine.name,
            'types': {},
        }
        information_types = SurveillanceManager.objects.filter(idMachine=machine).values_list('information_type', flat=True).distinct()
        for info_type in information_types:
            if info_type != "sysName" and info_type !="ifOperStatus" and info_type !="networkSpeed":
                data['types'][info_type] = SurveillanceManager.objects.filter(idMachine=machine, information_type=info_type)
            else :
                data['types'][info_type] = SurveillanceManager.objects.filter(idMachine=machine, information_type=info_type).latest("date")
            
        machines_data.append(data)
            
    return render(request, 'liste_donnees.html', {'machines_data': machines_data})



@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['login']
            
            user.set_password(form.cleaned_data['password'])
            
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            
            user.is_superuser = form.cleaned_data['is_admin']
            
            user.email = form.cleaned_data['mail']
            
            user.save()
            return redirect('liste_users')
    else:
        form = UtilisateurForm(initial={
            'login': user.username,  
            'password': user.password,  
            'last_name': user.last_name,
            'first_name': user.first_name,
            'is_admin': user.is_superuser, 
            'mail': user.email  
        })
    
    return render(request, 'edit_user.html', {'form': form})

def snmp_get(oid, host='localhost', community='public', timeout=1):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, 161), timeout=timeout),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(f"Erreur SNMP: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Erreur SNMP: {errorStatus} at {errorIndex}")
        return None
    else:
        return varBinds[0][1]    

@login_required
def json_test(request):
    chemin_fichier_json = os.path.join(settings.MEDIA_ROOT, 'config.json')
    
    with open(chemin_fichier_json, 'r') as fichier:
        contenu = json.load(fichier)
        oids = contenu.get("oids", {})  # Obtenez les OID à partir du fichier JSON
        machines = contenu.get("machines", [])
        for oid in contenu["oids"]:
            deja_existant = OID.objects.filter(name=oid).exists()
            if not deja_existant :
                OID.objects.create(name=oid, oid=contenu["oids"][oid]).save()
    snmp_results = {}
    for machine in machines:
        machine_name = machine.get("name")
        machine_ip = machine.get("ip")
        results = {}
        print(f"Machine: {machine_name}; Adresse IP : {machine_ip}")
        for oid_name, oid_value in oids.items():
            result = snmp_get(oid_value, host=machine_ip)
            if result is not None:
                print(f"{oid_name}: {result}")
                results[oid_name] = str(result)
            snmp_results[machine_name] = results
            print("\n")
    
    contenu["snmp_results"] = snmp_results

    with open(chemin_fichier_json, 'w') as fichier:
        json.dump(contenu, fichier, indent=4)       
        
    with open(chemin_fichier_json, 'r') as fichier:
        contenu = json.load(fichier)
        for a_oid in OID.objects.all() :
            for machine in contenu["snmp_results"]:
                if Machine.objects.filter(name=machine).exists():
                    SurveillanceManager.objects.create(idMachine=Machine.objects.get(name=machine), information_type=a_oid.name, data=contenu["snmp_results"][machine][a_oid.name])
    
    return redirect('donnees_machines')









