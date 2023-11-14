from .models import Machine, OID, SurveillanceManager, Logs, Graphique
from .forms import MachineForm, UtilisateurForm, OIDForm, GraphiqueForm, GetMachineForm
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

""" CRUD MACHINE """

@login_required
def add_machine(request):
    form = MachineForm()  # Initialiser le formulaire pour les requêtes GET

    if request.method == 'POST' and 'add_machine' in request.POST:
        form = MachineForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect("liste_machines")
        else:
            print(form.errors)

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
        print(form.errors)
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
        form = UtilisateurForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('liste_users')
    else:
        form = UtilisateurForm(instance=user)
    
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
    return render(request, 'liste_oids.html', {'oids': oids})

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
    graphiques = Graphique.objects.all().order_by('ordre')
    return render(request, 'liste_graphiques.html', {'graphiques': graphiques})

@login_required
def edit_graphique(request, graphique_id):
    graphique = get_object_or_404(Graphique, id=graphique_id)
    if request.method == 'POST':
        form = GraphiqueForm(request.POST, instance=graphique )
        if form.is_valid():
            form.save()
            return redirect('liste_graphiques')
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
    graphiques = Graphique.objects.all().order_by("ordre")
    
    machine = machines[0]

    if request.method == 'POST':
        form = GetMachineForm(request.POST)
        if form.is_valid():
            machine_select = form.cleaned_data['name']
            machine = Machine.objects.all().get(name=machine_select)
    else:
        form = GetMachineForm()
    
    data = {
        'name': machine,
        'types': {},
    }
    information_types = SurveillanceManager.objects.filter(idMachine=machine).values_list('information_type', flat=True).distinct()
    for info_type in information_types:
        if info_type != "sysName" and info_type !="ifOperStatus" and info_type !="networkSpeed" and info_type !="sysUpTime":
            data['types'][info_type] = SurveillanceManager.objects.filter(idMachine=machine, information_type=info_type)
        else :
            data['types'][info_type] = SurveillanceManager.objects.filter(idMachine=machine, information_type=info_type).latest("date")
            
    data_graphiques = []      
    
    for graphique in graphiques :
        list_temp = []
        if graphique.GraphiqueType == "Texte" :
            list_temp.append("Texte")
            list_temp.append(data["types"][graphique.OID1.name])
            list_temp.append(data["types"][graphique.OID1.name].data)
        else :
            list_temp.append("Fleche")
            list_temp.append(data["types"][graphique.OID1.name][0].information_type)
            liste_queryset = []
            for element in data["types"][graphique.OID1.name]:
                liste_queryset.append(element.data)
            list_temp.append(liste_queryset)
        data_graphiques.append(list_temp)
        
    return render(request, 'liste_donnees.html', {'data_graphiques': data_graphiques, 'machines' : machines, 'graphiques': graphiques, 'form': form})


@login_required
def logs(request):
    logs = Logs.objects.all()
    return render(request, 'liste_logs.html', {'logs': logs})
