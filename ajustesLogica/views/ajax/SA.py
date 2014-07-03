from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from ajustesLogica.Config import Configuracion
from ajustesLogica.models import SeguimientoSA, Ajuste
from ajustesLogica.views.ajustes.modelsCargaEvidencia import DocumentForm
import json

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def BuscarSAs(request):
    ajuste=json.loads(request.body)["Ajustes"]
    ID=int(ajuste['id'])
    sas=SeguimientoSA.objects.filter(AjusteAfectado__id=ID)
    if sas.__len__()>0:        
        sas=serializers.serialize("json",sas)
    else:
        sas=None
    
    response_data = {}
    response_data['error'] = False 
    response_data['mensaje'] = ""
    response_data['sas'] = sas
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def GrabarSAs(request):
    sa=json.loads(request.body)
    segsa=SeguimientoSA()
    error=False
    msg=""
    try:
        fecha=sa["fecha"]
        fecha=datetime.strptime(fecha,"%d/%m/%Y")
    except:
        error=True
        msg="La fecha esta en formato incorrecto, debe ser dd/mm/aaaa"
    if  not error:
        ajuste=Ajuste.objects.filter(id=sa["ajuste"])[0]
        segsa.AjusteAfectado=ajuste
        segsa.Folio=sa["folio"]
        segsa.Destinatario=sa["destinatario"]
        segsa.Puesto=sa["puesto"]
        segsa.Tema=sa["tema"]
        segsa.Fecha=fecha
        segsa.save()
    response_data = {}
    response_data['error'] = error
    response_data['mensaje'] = msg
    return HttpResponse(json.dumps(response_data), content_type="application/json")
