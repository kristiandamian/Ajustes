from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.core.mail import EmailMessage,send_mail, get_connection
from ajustesLogica.Config import Configuracion
from ajustesLogica.models import Ajuste, RegionAuditoria, Autorizacion, ImagenAjuste
import json

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def CanceloAjuste(request):
    ajustes=json.loads(request.body)["ids"]
    error=False
    msg=""
    for ID in ajustes:
        ajuste=Ajuste.objects.filter(id=ID)
        if ajuste.__len__()>0:
            ajuste=ajuste[0]
            
            ajuste.Activo=False
            ajuste.save()
    response_data = {}
    response_data['error'] = error 
    response_data['mensaje'] = msg
    response_data['data'] = None    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
