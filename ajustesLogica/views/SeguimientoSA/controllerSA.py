from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def SeguimientoSA(request):
    template = loader.get_template('SeguimientoSA/SA.html')
    context=RequestContext(request, {        
            'id':'0',
    })
    return HttpResponse(template.render(context))