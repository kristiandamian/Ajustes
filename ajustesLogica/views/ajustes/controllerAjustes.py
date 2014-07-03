from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from ajustesLogica.models import Ajuste, AjusteForm, CuentaAfectadaAjuste
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
                
            return HttpResponseRedirect('/ajustes/EvidenciaAjustes/{0}/'.format(str(ajuste.id)))
    
    context=RequestContext(request, {
        'forma':f,
        })
    template = loader.get_template(URI_TEMPLATE)
    return HttpResponse(template.render(context))

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

