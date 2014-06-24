from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from ajustesLogica.models import Ajuste, AjusteForm
from ajustesLogica.Config import Configuracion
from ajustesLogica.views.ajustes.modelsCargaEvidencia import DocumentForm

URI_TEMPLATE='ajustes/EvidenciaAjustes.html'

@login_required(login_url=Configuracion.LOGIN_URL)
def AltaEvidencia(request):
    return RenderViewEvidencia(request,None)
    

def AltaEvidenciaAjuste(request,ajuste):
    return RenderViewEvidencia(request,ajuste)

def RenderViewEvidencia(request,ajuste):
    template = loader.get_template(URI_TEMPLATE)
    busquedaAjuste=False
    if ajuste is None:
        busquedaAjuste=True
    
    form = DocumentForm()
    
    context=RequestContext(request, {
        'BusquedaAjuste':busquedaAjuste,
        'id':ajuste,
        'form': form,
        })
    return HttpResponse(template.render(context))