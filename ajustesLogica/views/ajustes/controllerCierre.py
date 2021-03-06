from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from ajustesLogica.models import Ajuste, AjusteForm,CierreAjuste, EmpleadosResponsables, ClasificacionAjuste, CierreAjuste
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def FinalizarAjuste(request):
    template = loader.get_template('ajustes/FinalizarAjuste.html')
    context=RequestContext(request, {
        'Estatus':CierreAjuste.TIPO_ESTATUS,
        'Laboral':EmpleadosResponsables.TIPO_ESTATUS_LABORAL,
        'TipoFraude':CierreAjuste.TIPO_FRAUDE[1:],
        'Clasificacion':ClasificacionAjuste.objects.all(),
    })
    return HttpResponse(template.render(context))