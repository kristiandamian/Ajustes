from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models import Count, Sum
from ajustesLogica.models import RegionAuditoria, Ajuste, ZonaAuditoria, ClasificacionAjuste, CierreAjuste 
from ajustesLogica.views.reportes.controllerAjustePorTipo import ValidoFechas
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def AjustePorClasificacionZona(request):
    template = loader.get_template('reportes/AjustePorClasificacion.html')
    zonas=ZonaAuditoria.objects.PorPermiso(request.user)
    clasificaciones=ClasificacionAjuste.objects.all()
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
        clasif=Clasificaciones(c.Clasificacion, c.Descripcion)
        for z in zonas:           
            index=ExisteElementoEnTotal(z.id,totales)
            if index<0:
                totales.append({z.id:[0,0.0]})
            cierres=CierreAjuste.objects.filter(Clasificacion=c,AjusteAfectado__Region__Zona=z,  AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal, AjusteAfectado__Activo=True)
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
        'Titulo':'Clasificacion de ajustes por tipo por zona',                
        'URL':'/ajustes/AjustePorClasificacionRegion/',
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
def AjustePorClasificacionRegion(request, zona_id):
    template = loader.get_template('reportes/AjustePorClasificacion.html')
    regiones=RegionAuditoria.objects.PorPermiso(request.user).filter(Zona__id=zona_id)
    clasificaciones=ClasificacionAjuste.objects.all()
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
        clasif=Clasificaciones(c.Clasificacion, c.Descripcion)
        for z in regiones:           
            index=ExisteElementoEnTotal(z.id,totales)
            if index<0:
                totales.append({z.id:[0,0.0]})
            cierres=CierreAjuste.objects.filter(Clasificacion=c,AjusteAfectado__Region=z,  AjusteAfectado__FechaRecepcion__gte=fechainicial, AjusteAfectado__FechaRecepcion__lte=fechafinal, AjusteAfectado__Activo=True)
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
        'Titulo':'Clasificacion de ajustes por tipo por region',                
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

def ExisteElementoEnTotal(llave, totales):
    existe=False
    pos=-1
    for t in totales:
        pos+=1
        if llave in t.keys():
            existe=True            
            break
    if not existe:
        pos=-1
    return pos

class Clasificaciones():
    nombre=""
    descripcion=""
    detalles=[]
    total=0
    monto=0.0
    def __init__(self, nombre, descripcion):
        self.nombre=nombre
        self.descripcion=descripcion
        self.detalles=[]
    
    def AddDetalle(self,detalle):
        self.detalles.append(detalle)
        
    def AddTotales(self,total,monto):
        self.total=total
        self.monto=monto

class DetalleClasificacion():
    total=0
    monto=0.0

    def __init__(self, total, monto):
        self.total=total
        self.monto=monto