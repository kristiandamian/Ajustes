from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from ajustesLogica.views.ajustes.controllerAutorizaciones import RenderAjuste
from ajustesLogica.Config import Configuracion
from ajustesLogica.models import Ajuste, UsuarioAcceso,RegionAuditoria

@login_required(login_url=Configuracion.LOGIN_URL)
@permission_required('ajustesLogica.Puede_Cancelar', raise_exception =True)
def CancelarAjuste(request):
    template = loader.get_template('soporte/Cancelacion.html')
    return RenderAjuste(request,template)