from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from ajustesLogica.Config import Configuracion
from ajustesLogica.models import Ajuste, CuentaAfectadaAjuste, CierreAjuste, EmpleadosResponsables
from ajustesLogica.views.ajustes.modelsCargaEvidencia import DocumentForm
import json

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def BuscarTodosLosAjustes(request):
    ajuste=json.loads(request.body)["Ajustes"]
    tienda=int(ajuste['tienda'])
    numcte=ajuste['numcte']
    error=False
    msg=""
    ajustes=None

    try:
        fechainicial=ajuste["fechaInicial"]
        fechainicial=datetime.strptime(fechainicial,"%d/%m/%Y")
    except:
        error=True
        msg="La fecha inicial esta en formato incorrecto, debe ser dd/mm/aaaa"
    try:
        fechafinal=ajuste["fechaFinal"]
        fechafinal=datetime.strptime(fechafinal,"%d/%m/%Y")
    except:
        error=True
        msg="La fecha final esta en formato incorrecto, debe ser dd/mm/aaaa"

    if type(fechainicial) is datetime and type(fechafinal) is datetime and fechainicial>=fechafinal:
        error=True
        msg ="La fecha final debe ser mayor a la fecha inicial"
    if not error:
        if numcte.__len__()>0:
            ajustes=Ajuste.objects.filter(Tienda=tienda, NumCte=int(numcte), FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion","Tienda","NumCte")
        else:
            ajustes=Ajuste.objects.filter(Tienda=tienda, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion","Tienda","NumCte")
        if ajustes.__len__()<=0:
            ajustes=None
        else:
            ajustes=serializers.serialize("json",ajustes)
    response_data = {}
    response_data['error'] = error 
    response_data['mensaje'] = msg
    response_data['ajustes'] = ajustes
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def BuscarNotasAjuste(request):    
    ajuste=json.loads(request.body)["Ajustes"]
    ID=int(ajuste['id'])
    empleados=None
    cuentas=CuentaAfectadaAjuste.objects.filter(AjusteAfectado__id=ID)
    datosCierre=CierreAjuste.objects.filter(AjusteAfectado__id=ID)    
    if cuentas.__len__()>0:        
        cuentas=serializers.serialize("json",cuentas)
    else:
        cuentas=None    
    if datosCierre.__len__()>0:
        empleados=EmpleadosResponsables.objects.filter(Cierre=datosCierre[0])
        datosCierre=serializers.serialize("json",datosCierre)
        if empleados.__len__()>0:
            empleados=serializers.serialize("json",empleados)
        else:
            empleados=None
    else:
        datosCierre=None
        
    response_data = {}
    response_data['error'] = False 
    response_data['mensaje'] = ""
    response_data['cuentas'] = cuentas
    response_data['datosCierre'] = datosCierre
    response_data['empleados'] = empleados
    response_data['TipoCentroCuenta']=CuentaAfectadaAjuste.TIPO_CENTRO
    response_data['EstatusCierre']=CierreAjuste.TIPO_ESTATUS
    response_data['EstatusLaboral']=EmpleadosResponsables.TIPO_ESTATUS_LABORAL
    response_data['TipoFraude']=CierreAjuste.TIPO_FRAUDE
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def BuscarAjustePorCte(request):
    ajuste=json.loads(request.body)["Ajustes"]    
    numcte=ajuste['numcte']
    error=False
    msg=""
    ajustes=None

    ajustes=Ajuste.objects.filter(NumCte=numcte).order_by("FechaRecepcion","Tienda","NumCte")
    if ajustes.__len__()<=0:
        ajustes=None
    else:
        ajustes=serializers.serialize("json",ajustes)
    response_data = {}
    response_data['error'] = error 
    response_data['mensaje'] = msg
    response_data['ajustes'] = ajustes
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")