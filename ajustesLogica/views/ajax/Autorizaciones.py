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
def RegistroAutorizacion(request):
    ajustes=json.loads(request.body)["ids"]
    error=False
    msg=""
    
    correos=ValidoCorreos(ajustes)
    
    if not correos[0]:
        error=True
        msg=" ".join(["Las siguientes regiones no tienen el correo correctamente configurado:",str(correos[1]).strip('[]')])
    else:
        for ID in ajustes:
            ajuste=Ajuste.objects.filter(id=ID)
            if ajuste.__len__()>0:
                ajuste=ajuste[0]
                aut=Autorizacion()
                aut.Usuario=request.user
                aut.AjusteAutorizado=ajuste
                aut.save()
                
                ajuste.Enviado=True
                ajuste.save()
                
                EnvioCorreo(request,ajuste,correos)
    response_data = {}
    response_data['error'] = error 
    response_data['mensaje'] = msg
    response_data['ajustes'] = None    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def ValidoCorreos(ids):
    error=True
    regiones_error=[]
    correos=[]
    for ID in ids:
        regiones_id=Ajuste.objects.filter(id=ID).values_list("Region__id",flat=True)
        regiones=RegionAuditoria.objects.filter(id__in=regiones_id)
        for r in regiones:
            if r.Correo==None or r.Password==None or r.Correo.__len__()==0 or r.Password.__len__()==0:
                error =False
                regiones_error.append(r.NombreRegion)
            else:
                correos.append((r.Correo,r.Password,r.id))
        regiones_error=sorted(set(regiones_error))
    return error, regiones_error, correos
        
def EnvioCorreo(request,ajuste,correos):
    usuario=""
    password=""
    titulo='Ajuste de auditoria'
    mensaje="Este es un mensaje de prueba para ver si el vaquero jala"
    for c in correos:
        if ajuste.Region.id==correos[2][0][2]:
            usuario=correos[2][0][0]
            password=correos[2][0][1]
            
    connection = get_connection(host=Configuracion.SMTP_SERVER, 
                                port=25, 
                                username=usuario, 
                                password=password)
    
    mensaje=EmailMessage(subject=titulo, body=mensaje, from_email=usuario,
        to=[Configuracion.CORREO_CARTERAS, ],bcc=[usuario,], connection=connection)
    
    for img in ImagenAjuste.objects.filter(CorrespondeAjuste=ajuste):        
        mensaje.attach_file(img.archivo.path)
    mensaje.send()
    


    