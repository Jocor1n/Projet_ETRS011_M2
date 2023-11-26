from .models import Machine, OID, SurveillanceManager, Logs
from django.conf import settings 
import os
import json
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.utils import timezone


def json_test():
    chemin_fichier_json = os.path.join(settings.MEDIA_ROOT, 'config.json')
    
    with open(chemin_fichier_json, 'r') as fichier:
        contenu = json.load(fichier)
        machines = Machine.objects.all()
        nouvelles_machines = []
        
        for machine in machines:
            nouvelles_machines.append({
                "name": machine.name,
                "ip": machine.IPAdresse
            })
        
        contenu["machines"] = nouvelles_machines
        
    with open(chemin_fichier_json, 'w') as fichier:
        json.dump(contenu, fichier, indent=4)  
        
    with open(chemin_fichier_json, 'r') as fichier:
        oids = OID.objects.all()
        oids_dict = {oid.name: oid.oid for oid in oids}
        contenu["oids"] = oids_dict
        
    with open(chemin_fichier_json, 'w') as fichier:
        json.dump(contenu, fichier, indent=4)

    def snmp_get_threaded(oid_name, oid_value, machine_ip):
        result = snmp_get(oid_value, host=machine_ip)
        return oid_name, result
  
    with open(chemin_fichier_json, 'r') as fichier:
        oids = contenu.get("oids", {})  # Obtenez les OID à partir du fichier JSON
        machines = contenu.get("machines", [])
    snmp_results = {}
    # Parcours des machines
    for machine in machines:
        machine_name = machine.get("name")
        machine_ip = machine.get("ip")
        results = {}
        print(f"{timezone.now()} Machine: {machine_name}; Adresse IP : {machine_ip}")
    
        # Création d'un pool de threads pour exécuter les requêtes SNMP
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_oid = {executor.submit(snmp_get_threaded, oid_name, oid_value, machine_ip): oid_name for oid_name, oid_value in oids.items()}
            print(timezone.now, future_to_oid)
            for future in as_completed(future_to_oid):
                oid_name, result = future.result()
                if result is not None:
                    print(f"{timezone.now()} {oid_name}: {result}")
                    results[oid_name] = str(result)
                elif oid_name == "ifOperStatus":
                    print(f"{timezone.now()} {oid_name}: 0")
                    results[oid_name] = str(0)
                    Logs.objects.create(idMachine=Machine.objects.get(name=machine_name), type_log="Error", informations="Hôte Non actif", is_error=True)
                
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
                    if a_oid.name in contenu["snmp_results"][machine]:
                        SurveillanceManager.objects.create(idMachine=Machine.objects.get(name=machine), information_type=a_oid.name, data=contenu["snmp_results"][machine][a_oid.name])
                        
   
def snmp_get(oid, host='localhost', community='public', timeout=1):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, 161), timeout=timeout),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )
    if errorIndication:
        print(f"{timezone.now()} Erreur SNMP: {errorIndication}")
        return None
    elif errorStatus:
        print(f"{timezone.now()} Erreur SNMP: {errorStatus} at {errorIndex}")
        return None
    else:
        return varBinds[0][1]    