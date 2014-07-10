from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from ajustesLogica.models import Ajuste, UsuarioAcceso, RegionAuditoria
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
            #zonas=UsuarioAcceso.objects.filter(Zona=userPermiso.Zona).values_list("Zona__id",flat=True)            
            regiones=RegionAuditoria.objects.filter(Zona__id__in=userPermiso.values_list("Zona__id",flat=True)).values_list("id",flat=True)
        ajustes=Ajuste.objects.filter(Q(Region__id__in=regiones)|Q(RegionRegistra__id__in=regiones), Enviado=False, Activo=True)

    context=RequestContext(request, {
        'ajustes':ajustes,
        'error':error,
        'mensaje':msg,
        })
    return HttpResponse(template.render(context))