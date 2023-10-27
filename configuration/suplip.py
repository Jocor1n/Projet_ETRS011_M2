import os

# Changez le répertoire de travail actuel vers la racine de votre projet
os.chdir("/home/azureuser/Django_APP/Projet_ETRS011_M2")

# Ensuite, vous pouvez importer Django et exécuter votre script
import django
from django.conf import settings

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supervision.settings")
django.setup()

# Importez vos modèles et écrivez votre code ici
from configuration.models import Machine  # Assurez-vous d'ajuster le chemin d'accès à vos modèles

def my_custom_function():
    machines = Machine.objects.all()
    for machine in machines:
        print(f"Nom : {machine.name}")
        print(f"Adresse IP : {machine.IPAdresse}")

if __name__ == "__main__":
    my_custom_function()
