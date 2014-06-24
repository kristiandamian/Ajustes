from django.contrib.auth.decorators import permission_required
from ajustesLogica.models import Ajuste, RegionAuditoria
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def ConfiguracionCorreo(request):
    template = loader.get_template('soporte/ConfigCorreo.html')
    regiones=RegionAuditoria.objects.PorPermiso(request.user).order_by("NombreRegion")
    context=RequestContext(request, {
        'regiones':regiones,
        })
    return HttpResponse(template.render(context))   