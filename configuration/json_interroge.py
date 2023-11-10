from .models import Machine, OID, SurveillanceManager
from django.conf import settings 
import os
import json
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

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

    with open(chemin_fichier_json, 'r') as fichier:
        oids = contenu.get("oids", {})  # Obtenez les OID à partir du fichier JSON
        machines = contenu.get("machines", [])
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