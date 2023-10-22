from django.http import HttpResponse
from .models import Machine, Utilisateur, OID, SurveillanceManager, Graphique, Logs
from .forms import MachineForm, UtilisateurForm
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    return render(request, 'index.html')

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
            return redirect("/configuration")
        else:
            print(form.errors)

    return render(request, 'configuration.html', {'form': form})

def add_user(request):
    form = UtilisateurForm()  # Initialiser le formulaire pour les requêtes GET

    if request.method == 'POST' and 'add_user' in request.POST:
        form = UtilisateurForm(request.POST)  
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']  
            last_name = form.cleaned_data['last_name']  
            first_name = form.cleaned_data['first_name']
            is_admin = form.cleaned_data['is_admin']
            mail = form.cleaned_data['mail']
            
            Utilisateur.objects.create(login=login, password=password, last_name=last_name, first_name=first_name, is_admin=is_admin, mail=mail)
            return redirect("/configuration")
        else:
            print(form.errors)

    return render(request, 'utilisateur.html', {'form': form})

def liste_machines(request):
    machines = Machine.objects.all()
    return render(request, 'liste_machines.html', {'machines': machines})


def liste_users(request):
    users = Utilisateur.objects.all()
    return render(request, 'liste_users.html', {'users': users})

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

def delete_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    if request.method == 'POST':
        machine.delete()
        return redirect('liste_machines')
    return render(request, 'confirm_delete.html', {'object': machine})

def edit_user(request, user_id):
    form = UtilisateurForm()
    user = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            user.login = form.cleaned_data['login']
            user.password = form.cleaned_data['password']  
            user.last_name = form.cleaned_data['last_name']  
            user.first_name = form.cleaned_data['first_name']
            user.is_admin = form.cleaned_data['is_admin']
            user.mail = form.cleaned_data['mail']
            user.save()
            return redirect('liste_users')
    else:
        form = UtilisateurForm(initial={
        'login' : user.login,
        'password' : user.password,
        'last_name' : user.last_name,
        'first_name' : user.first_name,
        'is_admin' : user.is_admin,
        'mail' : user.mail
        })
    return render(request, 'edit_user.html', {'form': form})

def delete_user(request, user_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('liste_users')
    return render(request, 'confirm_delete.html', {'object': user})



