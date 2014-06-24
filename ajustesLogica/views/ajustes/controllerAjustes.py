from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from ajustesLogica.models import Ajuste, AjusteForm
from ajustesLogica.Config import Configuracion

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
        if f.is_valid():
            ajuste=f.save(commit=False)
            ajuste.Usuario=request.user
            ajuste.save()
            return HttpResponseRedirect('/ajustes/EvidenciaAjustes/{0}/'.format(str(ajuste.id)))
    
    context=RequestContext(request, {
        'forma':f,
        })
    template = loader.get_template(URI_TEMPLATE)
    return HttpResponse(template.render(context))