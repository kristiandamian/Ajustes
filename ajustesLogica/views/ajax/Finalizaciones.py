from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.core.mail import EmailMessage,send_mail, get_connection
from ajustesLogica.Config import Configuracion
from ajustesLogica.models import Ajuste, RegionAuditoria, Autorizacion, ImagenAjuste, CierreAjuste, EmpleadosResponsables, ClasificacionAjuste
import json

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def FinalizacionAjuste(request):    
    aj=json.loads(json.loads(request.body))
    error=False
    msg=""
    NO_FRAUDE=0
    ajuste=Ajuste.objects.filter(id=aj["id"])
    if ajuste.__len__()>0:
        clas=ClasificacionAjuste.objects.filter(id=aj["clasificacion"])
        if clas.__len__()>0:
            clas=clas[0]
            ajuste=ajuste[0]
            ajuste.Finalizado=True
            if aj["procede"]:
                ajuste.ProcedeAjuste=True
            else:
                ajuste.NoProcedeAjuste=True
            ajuste.save()            
            
            cierre=CierreAjuste()
            cierre.AjusteAfectado=ajuste
            cierre.Clasificacion=clas
            cierre.Observaciones=aj["observacion"]
            cierre.Estatus=aj["estatus"]
            cierre.Usuario=request.user
            cierre.EsFraude=aj["esfraude"]
            if not cierre.EsFraude:
                cierre.TipoFraude=NO_FRAUDE
            else:
                cierre.TipoFraude=aj["tipofraude"]
            cierre.save()
            
            for emp in aj["empleados"]:
                responsable=EmpleadosResponsables()
                responsable.Cierre=cierre
                responsable.NumEmpleado=emp["NumEmp"]
                responsable.NomEmpleado=emp["NombreEmp"]
                responsable.EstatusLaboral=emp["Estatus"]
                responsable.save()
        else:
            msg="No existe la clasificacion"
            error=True
    else:
        msg="No existe el ajuste"
        error=True
    response_data = {}
    response_data['error'] = error
    response_data['mensaje'] = msg
    response_data['data'] = None
    return HttpResponse(json.dumps(response_data), content_type="application/json")