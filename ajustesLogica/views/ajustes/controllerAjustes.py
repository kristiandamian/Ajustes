from datetime import datetime
from django.core.mail import EmailMessage,send_mail, get_connection
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from ajustesLogica.models import Ajuste, AjusteForm, CuentaAfectadaAjuste, RegionAuditoria
from ajustesLogica.Config import Configuracion
import json

URI_TEMPLATE='ajustes/RegistrarAjustes.html'

@login_required(login_url=Configuracion.LOGIN_URL)
def AltaAjuste(request):
    template = loader.get_template(URI_TEMPLATE)
    fechaActual =  str(datetime.now().day)+"/"+str(datetime.now().month)+"/"+str(datetime.now().year)
    form=AjusteForm(initial={'NumCuentas': 1,'FechaRecepcion':fechaActual})    
    context=RequestContext(request, {
        'forma':form,        
        })
    return HttpResponse(template.render(context))

@login_required(login_url=Configuracion.LOGIN_URL)
def RegistrarAjuste(request):
    f=AjusteForm(request.POST)    
    if request.method=='POST':
        ajustes=json.loads(request.POST['jsonTable'])
        if f.is_valid():
            ajuste=f.save(commit=False)
            ajuste.Usuario=request.user
            ajuste.save()
            for d in ajustes["datos"]:
                caa = CuentaAfectadaAjuste()
                caa.AjusteAfectado = ajuste
                caa.Tipo = d['tipo']
                caa.Factura = d['factura']
                caa.Tienda = d['tienda']
                caa.Monto = d['monto']
                caa.Fecha = datetime.strptime(d['fecha'],"%d/%m/%Y")
                caa.save()
            if ajuste.RegionRegistra!=ajuste.Region:
                EnvioCorreoOtraRegion(ajuste)
            return HttpResponseRedirect('/ajustes/EvidenciaAjustes/{0}/'.format(str(ajuste.id)))
    context=RequestContext(request, {
        'forma':f,
        })
    template = loader.get_template(URI_TEMPLATE)
    return HttpResponse(template.render(context))

def EnvioCorreoOtraRegion(ajuste):
    usuario=""
    password=""
    titulo="Ajuste de auditoria desde otra region: "+ajuste.RegionRegistra.NombreRegion
    mensaje="""
                Buen dia.
                
                Te informo del registro de la solicitud de ajuste del cliente # """+str(ajuste.NumCte)+""" mismo que no reconoce las compras afectando su credito en """+str(ajuste.NumCuentas)+""" Cuenta(s)
                El detalle de este ajuste lo encontraras en el sistema de gestion de ajustes
                En caso de cualquier duda o aclaracion, estamos a tus ordenes
                
                Saludos cordiales
                
                """+ajuste.RegionRegistra.GerenteRegion+"""
                Region """+ajuste.RegionRegistra.NombreRegion+"""
                
                *** Este es un correo autogenerado ***
            """
    destino=RegionAuditoria.objects.filter(id=ajuste.Region.id)
    origen=RegionAuditoria.objects.filter(id=ajuste.RegionRegistra.id)

    if destino.__len__()>0 and origen.__len__()>0:
        destino=destino[0]
        origen=origen[0]
        usuario=origen.Correo
        password=origen.Password
        
        connection = get_connection(host=Configuracion.SMTP_SERVER,
                                    port=25,
                                    username=usuario,
                                    password=password)
        
        mensaje=EmailMessage(subject=titulo, body=mensaje, from_email=usuario,
            to=[destino.Correo, ], connection=connection)    
        mensaje.send()

@login_required(login_url=Configuracion.LOGIN_URL)
def VerAjustes(request):
    return RenderVerAjuste(request,None)

@login_required(login_url=Configuracion.LOGIN_URL)
def VerAjuste(request, ajuste):
    return RenderVerAjuste(request,ajuste)

def RenderVerAjuste(request, ajuste):
    template = loader.get_template('ajustes/VerAjuste.html')
    busquedaAjuste=False
    if ajuste is None:
        busquedaAjuste=True
    context=RequestContext(request, {
        'forma':None,
        'id':ajuste,
        'BusquedaAjuste':busquedaAjuste,
        })
    return HttpResponse(template.render(context))

