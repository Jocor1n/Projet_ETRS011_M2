from django.http import HttpResponse
from .models import Machine, Utilisateur, OID, SurveillanceManager, Graphique, Logs
from .forms import Configuration
from django.template import loader

def index(request):
    if request.method == 'POST' and 'add_message' in request.POST:
        form = Configuration(request.POST)
        if form.is_valid():
            current_message = form.cleaned_data['name']
            print(current_message)
            #StudioRadio.objects.update(messageCourant_text=current_message)
    template = loader.get_template('configuration.html')
    context = {}
    return HttpResponse(template.render(context, request))