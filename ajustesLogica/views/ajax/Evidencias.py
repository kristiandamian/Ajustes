from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from ajustesLogica.Config import Configuracion
from ajustesLogica.models import Ajuste, ImagenAjuste
from ajustesLogica.views.ajustes.modelsCargaEvidencia import DocumentForm
import json

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def BuscarAjustes(request):
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
def BuscarAjuste(request):
    ajuste=json.loads(request.body)["Ajustes"]
    ID=int(ajuste['id'])
    error=False
    msg=""
    ajustes=Ajuste.objects.filter(id=ID).order_by("FechaRecepcion","Tienda","NumCte")
    if ajustes.__len__()<=0:
        ajustes=None
    else:
        ajustes=serializers.serialize("json",ajustes)
    #json completo para seguir el estandar 
    response_data = {}
    response_data['error'] = error 
    response_data['mensaje'] = msg
    response_data['ajustes'] = ajustes
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def upload(request):
    response_data = {}
    
    error=True
    msg="Ocurrio un error al subir el archivo"
    
    if request.is_ajax():
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            ajuste=Ajuste.objects.filter(id=request.POST["ajuste"])
            if ajuste.__len__()>0:
                ajuste=ajuste[0]
                upload = ImagenAjuste()
                upload.archivo = request.FILES["docfile"]
                upload.Imagen = request.FILES["docfile"]
                upload.Usuario=request.user
                                
                upload.CorrespondeAjuste=ajuste
                upload.save()
    
                error = False
                msg = "Se ha anexado el archivo:"
                #msg = "Se ha anexado el archivo:/%s" % upload.upload
            else:
                msg="No existe el ajuste seleccionado"
        else:
            msg=form.messages
    else:
        msg="Metodo incorrecto para subir el archivo"
    

    response_data['error'] = error
    response_data['mensaje'] = msg
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required(login_url=Configuracion.LOGIN_URL)
@csrf_exempt
def BuscarEvidencias(request):
    ajuste=ImagenAjuste.objects.filter(CorrespondeAjuste__id=request.POST["ajuste"])
    ajustes=[]
    
    for a in ajuste:
        ajustes.append(a.archivo.name)
        
    response_data = {}        
    response_data['error'] = False 
    response_data['mensaje'] = ""
    response_data['ajustes'] = ajustes
    return HttpResponse(json.dumps(response_data), content_type="application/json")
