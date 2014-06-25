from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models.aggregates import Sum
from ajustesLogica.models import RegionAuditoria, Ajuste
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def AjustesPorFecha(request):
    template = loader.get_template('reportes/AjustesPorFecha.html')
    regiones=RegionAuditoria.objects.PorPermiso(request.user).order_by("NombreRegion")
    
    region=-1
    tda=""
    fechainicial=""
    fechafinal=""
    error=False
    msg=""
    datos=None
    if request.method == 'POST':
        tda=request.POST["txtTienda"]
        region=request.POST["cmbRegion"]        
        try:
            fechainicial=request.POST["fechaInicial"]
            fechainicial=datetime.strptime(fechainicial,"%d/%m/%Y")
        except:
            error=True
            msg="La fecha inicial esta en formato incorrecto, debe ser dd/mm/aaaa"
        try:
            fechafinal=request.POST["fechaFinal"]
            fechafinal=datetime.strptime(fechafinal,"%d/%m/%Y")
        except:
            error=True
            msg="La fecha final esta en formato incorrecto, debe ser dd/mm/aaaa"

        try:
            tda=int(tda)
        except:
            tda=0
            
        if type(fechainicial) is datetime and type(fechafinal) is datetime and fechainicial>=fechafinal:
            error=True
            msg ="La fecha final debe ser mayor a la fecha inicial"
        if not error:
            if tda>0:
                datos=Ajuste.objects.filter(Tienda=tda, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion","Tienda")
            else:
                if int(region)>0:
                        datos=Ajuste.objects.filter(Region__id=region, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion","Tienda")
                else:
                    datos=Ajuste.objects.filter(FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion","Tienda")
                
    context=RequestContext(request, {
                'regiones':regiones,
                'Datos':datos,
                'FechaInicial':fechainicial,
                'FechaFinal':fechafinal,
                'Tienda':tda,
                'Error':error,
                'MensajeError':msg,
                'Region':int(region),
        })
    return HttpResponse(template.render(context)) 