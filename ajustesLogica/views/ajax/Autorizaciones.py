from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Count
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
        anexos=ValidoAnexos(ajustes)
        if not anexos[0]:
            error=True
            msg=" ".join(["Los siguientes ajustes no tienen informacion anexa que soporte el ajuste:",str(anexos[1]).strip('[]')])            
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
    response_data["error"] = error
    response_data["mensaje"] = msg
    response_data["ajustes"] = None
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

def ValidoAnexos(ids):
    error=True
    regiones_error=[]    
    for ID in ids:
        ajuste=Ajuste.objects.filter(id=ID)        
        for r in ajuste:
            total=ImagenAjuste.objects.filter(CorrespondeAjuste=r).values('Imagen').annotate(total = Count('Imagen'))

            print total
            print total.__len__()
            if total.__len__()==0:
                error =False
                regiones_error.append("-Cte:"+str(r.NumCte)+" por el monto "+str(r.Monto))
        regiones_error=sorted(set(regiones_error))
    return error, regiones_error

def EnvioCorreo(request,ajuste,correos):
    usuario=""
    password=""
    titulo="Ajuste de auditoria"
    mensaje="""
                Buen dia.
                
                Te envio la solicitud de ajuste del cliente # """+str(ajuste.NumCte)+""" mismo que no reconoce las compras afectando su credito en """+str(ajuste.NumCuentas)+""" Cuenta(s)
                Anexo encontraras la documentacion digital que corresponde a este ajuste.
                En caso de cualquier duda o aclaracion, estamos a tus ordenes
                
                Saludos cordiales
                
                """+ajuste.Region.GerenteRegion+"""
                Region """+ajuste.Region.NombreRegion+"""
                
                *** Este es un correo autogenerado ***
            """
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
    