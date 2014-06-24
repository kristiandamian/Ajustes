from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import Http404
from ajustesLogica.models import Ajuste, UsuarioAcceso
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
@permission_required('ajustesLogica.Puede_Autorizar', raise_exception =True)
def AutorizarAjustes(request):
    template = loader.get_template('ajustes/Autorizacion.html')
    return RenderAjuste(request,template)

def RenderAjuste(request, template):
    error=False
    msg=""
    ajustes=None    
    userPermiso=UsuarioAcceso.objects.filter(Usuario=request.user)
    
    if userPermiso.__len__()<=0 or (userPermiso[0].Region==None and userPermiso[0].Zona==None):
        error=True
        msg="El usuario no tiene una region o zona asignada"
    else:
        #userPermiso=userPermiso[0]
        regiones=[]
        if userPermiso[0].Region!=None:
            regiones=userPermiso.values_list("Region__id",flat=True)
        else:
            regiones=RegionAuditoria.objects.filter(Region__Zona=userPermiso.Zona).values_list("Region__id",flat=True)

        ajustes=Ajuste.objects.filter(Region__id__in=regiones, Enviado=False, Activo=True)

    context=RequestContext(request, {
        'ajustes':ajustes,
        'error':error,
        'mensaje':msg,
        })
    return HttpResponse(template.render(context))