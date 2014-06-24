from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from ajustesLogica.Config import Configuracion
from ajustesLogica.models import RegionAuditoria
import json

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def BuscarCorreo(request):
    region=RegionAuditoria.objects.filter(id=request.POST["region"])
    correo=""
    if region.__len__()>0:
        region=region[0]
        correo=region.Correo
    response_data = {}        
    response_data['error'] = False 
    response_data['mensaje'] = ""
    response_data['data'] = correo
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def GrabarCorreo(request):
    datos=json.loads(request.body)
    region=RegionAuditoria.objects.filter(id=datos["id"])
    error=False
    msg=""
    if region.__len__()>0:
        region=region[0]
        region.Correo=datos["usr"]
        region.Password=datos["psw"]
        region.save()
    else:
        error=True
        msg="No esta registrada la region seleccionada"
    response_data = {}        
    response_data['error'] = error 
    response_data['mensaje'] = msg
    response_data['data'] = None
    return HttpResponse(json.dumps(response_data), content_type="application/json")
