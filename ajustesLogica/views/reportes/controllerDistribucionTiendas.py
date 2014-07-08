from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models.aggregates import Sum, Count
from django.db.models import Q
from ajustesLogica.models import RegionAuditoria, Ajuste, CuentaAfectadaAjuste
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def DistribucionTienda(request):
    template = loader.get_template('reportes/DistribucionTienda.html')
    regiones=RegionAuditoria.objects.PorPermiso(request.user).order_by("NombreRegion")
    
    resultados=[]
    generar=False
    region=-1    
    fechainicial=""
    fechafinal=""
    error=False
    msg=""    
    PorNumeroAjustes=False
    if request.method == 'POST':
        generar=True        
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
            region=int(region)
        except:
            error=True
            msg="Region incorrecta"
            
        if type(fechainicial) is datetime and type(fechafinal) is datetime and fechainicial>=fechafinal:
            error=True
            msg ="La fecha final debe ser mayor a la fecha inicial"
        if not error:
            campo=""
            print 

        if not PorNumeroAjustes:
            datos=CuentaAfectadaAjuste.objects.filter(AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal).order_by("Tienda").values('Tienda').annotate(Cargo=Sum('Monto'))
        else:
            datos=CuentaAfectadaAjuste.objects.filter(AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal).order_by("Tienda").values('Tienda').annotate(Cargo=Count('Tienda', distinct=True))
        
        if region>0:
            datos=datos.filter(AjusteAfectado__Region__id=region)
        
        for d in datos:
            resultados.append((d['Tienda'],d['Cargo']))
                
    context=RequestContext(request, {
                'regiones':regiones,
                'Datos':resultados,
                'Generar':generar,        
                'FechaInicial':fechainicial,
                'FechaFinal':fechafinal,                
                'Error':error,
                'MensajeError':msg,
                'Region':int(region),
                'PorNumeroAjustes':PorNumeroAjustes,
        })
    return HttpResponse(template.render(context))

