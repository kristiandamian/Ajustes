from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models.aggregates import Sum, Count
from ajustesLogica.models import RegionAuditoria, Ajuste
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def TendenciasAjustes(request):
    template = loader.get_template('reportes/GraficaTendencias.html')
    regiones=RegionAuditoria.objects.PorPermiso(request.user).order_by("NombreRegion")
    
    resultados=[]
    generar=False
    region=-1
    tda=""
    fechainicial=""
    fechafinal=""
    error=False
    msg=""
    daysDiff=Configuracion.DAYS_DIFF
    
    if request.method == 'POST':
        generar=True
        tda=request.POST["txtTienda"]
        region=request.POST["cmbRegion"]
        datos=None
        PorNumeroAjustes=request.POST.get('NumAjustes', False)
        
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
            daysDiff = fechafinal-fechainicial
            daysDiff = daysDiff.days
            campo=""            
            if int(region)>0:
                if not PorNumeroAjustes:
                    if tda>0:
                        datos=Ajuste.objects.filter(Tienda=tda, Region__id=region, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion").values('FechaRecepcion').annotate(Cargo=Sum('Monto'))
                    else:
                        datos=Ajuste.objects.filter(Region__id=region, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion").values('FechaRecepcion').annotate(Cargo=Sum('Monto'))
                else:
                    if tda>0:
                        datos=Ajuste.objects.filter(Tienda=tda, Region__id=region, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion").values('FechaRecepcion').annotate(Cargo=Count('FechaRecepcion'))
                    else:
                        datos=Ajuste.objects.filter(Region__id=region, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal).order_by("FechaRecepcion").values('FechaRecepcion').annotate(Cargo=Count('FechaRecepcion'))
            else:
                error=True
                msg="Debe seleccionar una region"
            for d in datos:
                resultados.append((d['FechaRecepcion'],d['Cargo']))
                
    context=RequestContext(request, {
                'regiones':regiones,
                'Datos':resultados,
                'Generar':generar,        
                'FechaInicial':fechainicial,
                'FechaFinal':fechafinal,
                'Tienda':tda,
                'DiasEntreFechas':daysDiff<Configuracion.MAX_DAYS_DIFF,
                'Error':error,
                'MensajeError':msg,
                'Region':int(region),
        })
    return HttpResponse(template.render(context))   