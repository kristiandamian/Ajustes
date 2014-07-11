from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models import Count, Sum
from ajustesLogica.models import RegionAuditoria, Ajuste, ZonaAuditoria, ClasificacionAjuste, CierreAjuste 
from ajustesLogica.views.reportes.controllerAjustePorTipo import ValidoFechas
from ajustesLogica.views.reportes.controllerAjustePorClasificacionZona import Clasificaciones, DetalleClasificacion, ExisteElementoEnTotal
from ajustesLogica.Config import Configuracion

TEMPLATE_URI='reportes/AjustePorFraude.html'
@login_required(login_url=Configuracion.LOGIN_URL)
def AjustePorFraudeZona(request):
    template = loader.get_template(TEMPLATE_URI)
    zonas=ZonaAuditoria.objects.PorPermiso(request.user)
    clasificaciones=CierreAjuste.TIPO_FRAUDE
    datos=[]
    totales=[]
    error=False
    msg=""
    fechainicial=datetime.min
    fechafinal=datetime.max
    totalClasificacion=0
    montoClasificacion=float(0)
    granTotal=0
    granTotalMonto=float(0)
    if request.method == 'POST':
        datosValidacion=ValidoFechas(request)##DEVUELVE: error, msg, fechainicial, fechafinal
        error=datosValidacion[0]
        msg=datosValidacion[1]
        fechainicial=datosValidacion[2]
        fechafinal=datosValidacion[3]
    
    for c in clasificaciones:
        totalClasificacion=0
        montoClasificacion=0
        clasif=Clasificaciones(c[1],c[0])
        for z in zonas:
            index=ExisteElementoEnTotal(z.id,totales)
            if index<0:
                totales.append({z.id:[0,0.0]})
            cierres=CierreAjuste.objects.filter(TipoFraude=c[0],AjusteAfectado__Region__Zona=z,  AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal, AjusteAfectado__Activo=True)
            total=cierres.values('AjusteAfectado__Region__Zona') \
                      .annotate(total = Count('AjusteAfectado__Tienda'))
            monto=cierres.values('AjusteAfectado__Region__Zona') \
                      .annotate(total = Sum('AjusteAfectado__Monto'))
            if total.__len__()>0:
                total=total[0]["total"]
            else:
                total=0
            if monto.__len__()>0:
                monto=monto[0]["total"]
            else:
                monto=0
            totalClasificacion+=total
            montoClasificacion+=float(monto)
            detalle=DetalleClasificacion( total,monto)
            clasif.AddDetalle(detalle)
            
            totales[index][z.id][0]+=total
            totales[index][z.id][1]+=float(monto)
            
            granTotal+=total
            granTotalMonto+=float(monto)
        clasif.AddTotales(totalClasificacion,montoClasificacion)
        datos.append(clasif)
    
    if fechainicial==datetime.min:
        fechainicial=None
    if fechafinal==datetime.max:
        fechafinal=None
    
    context = RequestContext(request, {
        'Titulo':'Clasificacion de ajustes por tipo por fraudes',                
        'URL':'/ajustes/AjustePorFraudeRegion/',
        'Zonas':zonas,
        'Datos':datos,
        'Totales':totales,
        'Error':error,        
        'MensajeError':msg,
        'FechaInicial':fechainicial,
        'FechaFinal':fechafinal,
        'granTotal':granTotal,
        'granTotalMonto':granTotalMonto,
    })
    return HttpResponse(template.render(context))

@login_required(login_url=Configuracion.LOGIN_URL)
def AjustePorFraudeRegion(request, zona_id):
    template = loader.get_template(TEMPLATE_URI)
    regiones=RegionAuditoria.objects.PorPermiso(request.user).filter(Zona__id=zona_id)
    clasificaciones=CierreAjuste.TIPO_FRAUDE
    datos=[]
    totales=[]
    error=False
    msg=""
    fechainicial=datetime.min
    fechafinal=datetime.max
    totalClasificacion=0
    montoClasificacion=float(0)
    granTotal=0
    granTotalMonto=float(0)
    if request.method == 'POST':
        datosValidacion=ValidoFechas(request)##DEVUELVE: error, msg, fechainicial, fechafinal
        error=datosValidacion[0]
        msg=datosValidacion[1]
        fechainicial=datosValidacion[2]
        fechafinal=datosValidacion[3]    
    for c in clasificaciones:        
        totalClasificacion=0
        montoClasificacion=0        
        clasif=Clasificaciones(c[1],c[0])
        for z in regiones:           
            index=ExisteElementoEnTotal(z.id,totales)
            if index<0:
                totales.append({z.id:[0,0.0]})
            cierres=CierreAjuste.objects.filter(TipoFraude=c[0],AjusteAfectado__Region=z,  AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal, AjusteAfectado__Activo=True)
            total=cierres.values('AjusteAfectado__Region__Zona') \
                      .annotate(total = Count('AjusteAfectado__Tienda'))
            monto=cierres.values('AjusteAfectado__Region__Zona') \
                      .annotate(total = Sum('AjusteAfectado__Monto'))
            if total.__len__()>0:
                total=total[0]["total"]
            else:
                total=0
            if monto.__len__()>0:
                monto=monto[0]["total"]
            else:
                monto=0
            totalClasificacion+=total
            montoClasificacion+=float(monto)
            detalle=DetalleClasificacion( total,monto)
            clasif.AddDetalle(detalle)
            
            totales[index][z.id][0]+=total
            totales[index][z.id][1]+=float(monto)
            
            granTotal+=total
            granTotalMonto+=float(monto)
        clasif.AddTotales(totalClasificacion,montoClasificacion)
        datos.append(clasif)
    
    if fechainicial==datetime.min:
        fechainicial=None
    if fechafinal==datetime.max:
        fechafinal=None
    
    context = RequestContext(request, {
        'Titulo':'Clasificacion de ajustes por fraude por region',                
        'URL':None,
        'Zonas':None,
        'Regiones':regiones,
        'Datos':datos,
        'Totales':totales,
        'Error':error,        
        'MensajeError':msg,
        'FechaInicial':fechainicial,
        'FechaFinal':fechafinal,
        'granTotal':granTotal,
        'granTotalMonto':granTotalMonto,
    })
    return HttpResponse(template.render(context))
