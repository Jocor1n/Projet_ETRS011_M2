#!/usr/bin/env python
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd
import json
# Lisez les OID à partir du fichier JSON
with open('config.json') as json_file:

    config_data = json.load(json_file)
    oids = config_data.get("oids", {})  # Obtenez les OID à partir du fichier JSON
    machines = config_data.get("machines", [])

print(json.dumps(config_data, indent=4))

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

snmp_results = {}

for machine in machines:
    machine_name = machine.get("name")
    machine_ip = machine.get("ip")
    results = {}
    # Affichez le nom de la machine et l'adresse IP
    print(f"Machine: {machine_name}; Adresse IP : {machine_ip}")
    # Utilisez la fonction snmp_get avec l'adresse IP de la machine
    for oid_name, oid_value in oids.items():
        result = snmp_get(oid_value, host=machine_ip)
       # print(f"result : {result} oidname :{oid_name} oid_value : {oid_value}")
        if result is not None:
            print(f"{oid_name}: {result}")
            results[oid_name] = str(result)  # Convertissez la valeur en chaîne si nécessaire
    snmp_results[machine_name] = results
    print("\n")

config_data["snmp_results"] = snmp_results

# Ensuite, réécrivez le fichier JSON avec les données mises à jour
with open('config.json', 'w') as json_file:
    json.dump(config_data, json_file, indent=4)

