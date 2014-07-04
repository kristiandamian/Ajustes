from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models.aggregates import Sum, Count
from ajustesLogica.models import RegionAuditoria, Ajuste, CuentaAfectadaAjuste
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def DistribucionCentro(request):
    template = loader.get_template('reportes/DistribucionCentro.html')
    regiones=RegionAuditoria.objects.PorPermiso(request.user).order_by("NombreRegion")
    
    resultados=[]
    generar=False
    region=-1
    tda=""
    fechainicial=""
    fechafinal=""
    error=False
    msg=""    
    PorNumeroAjustes=False
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
            campo=""            
            if int(region)>0:
                if not PorNumeroAjustes:
                    if tda>0:
                        datos=CuentaAfectadaAjuste.objects.filter(AjusteAfectado__Tienda=tda, AjusteAfectado__Region__id=region, AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal).order_by("Tipo").values('Tipo').annotate(Cargo=Sum('AjusteAfectado__Monto'))
                    else:
                        datos=CuentaAfectadaAjuste.objects.filter(AjusteAfectado__Region__id=region, AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal).order_by("Tipo").values('Tipo').annotate(Cargo=Sum('AjusteAfectado__Monto'))
                else:
                    if tda>0:
                        datos=CuentaAfectadaAjuste.objects.filter(AjusteAfectado__Tienda=tda, AjusteAfectado__Region__id=region, AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal).order_by("Tipo").values('Tipo').annotate(Cargo=Count('Tipo'))
                    else:
                        datos=CuentaAfectadaAjuste.objects.filter(AjusteAfectado__Region__id=region, AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal).order_by("Tipo").values('Tipo').annotate(Cargo=Count('Tipo'))
            else:
                error=True
                msg="Debe seleccionar una region"
            for d in datos:
                resultados.append((NombreTipo(d['Tipo']),d['Cargo']))
                
    context=RequestContext(request, {
                'regiones':regiones,
                'Datos':resultados,
                'Generar':generar,        
                'FechaInicial':fechainicial,
                'FechaFinal':fechafinal,
                'Tienda':tda,
                'Error':error,
                'MensajeError':msg,
                'Region':int(region),
                'PorNumeroAjustes':PorNumeroAjustes,
        })
    return HttpResponse(template.render(context))

def NombreTipo(estatus):
    nom=""
    for t in CuentaAfectadaAjuste.TIPO_CENTRO:
        if t[0]==estatus:
            nom=t[1]
    return nom
    
    
