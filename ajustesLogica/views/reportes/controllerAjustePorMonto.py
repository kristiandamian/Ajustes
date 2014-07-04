from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models import Sum
from ajustesLogica.models import RegionAuditoria, Ajuste, ZonaAuditoria
from ajustesLogica.Config import Configuracion

URI_TEMPLATE='reportes/AjustesPorMonto.html'

@login_required(login_url=Configuracion.LOGIN_URL)
def AjustePorMontoZona(request):
    template = loader.get_template(URI_TEMPLATE)
    zonas=ZonaAuditoria.objects.PorPermiso(request.user)
    Titulos=["Registrados","Activos","Sin autorizar","Enviados","Cancelados","Procede ajuste","No Procede ajuste"]
    datos=[]
    totales=[]
    totalReg=0
    totalAct=0
    totalSinAut=0
    totalEnv=0
    totalCanc=0
    totalProc=0
    totalNoProc=0
    fechainicial=datetime.min
    fechafinal=datetime.max
    error=False
    msg=""
    if request.method == 'POST':
        datosValidacion=ValidoFechas(request)##DEVUELVE: error, msg, fechainicial, fechafinal
        error=datosValidacion[0]
        msg=datosValidacion[1]
        fechainicial=datosValidacion[2]
        fechafinal=datosValidacion[3]
        
    for z in zonas:
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region__Zona') \
                      .annotate(total = Sum('Monto')))
        ajuste=AjusteTipo(z.id,z.NombreZona)
        tipo=TipoEspecifico("Registrados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalReg+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Activo=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region__Zona') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Activos",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalAct+=ajustes[0]["total"]

        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Enviado=False, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region__Zona') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Sin autorizar",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalSinAut+=ajustes[0]["total"]

        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Enviado=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region__Zona') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Enviados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalEnv+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Activo=False, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region__Zona') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Cancelados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalCanc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,ProcedeAjuste=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region__Zona') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Procede ajuste",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalProc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,NoProcedeAjuste=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region__Zona') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("No Procede ajuste",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalNoProc+=ajustes[0]["total"]
        
        datos.append(ajuste)
    totales.append(totalReg)
    totales.append(totalAct)
    totales.append(totalSinAut)
    totales.append(totalEnv)
    totales.append(totalCanc)
    totales.append(totalProc)
    totales.append(totalNoProc)
    
    if fechainicial==datetime.min:
        fechainicial=None
    if fechafinal==datetime.max:
        fechafinal=None
        
    context = RequestContext(request, {
        'Titulo':'Ajustes por monto por zona',        
        'Encabezado':'Zona',
        'URL':'/ajustes/AjustePorMontoRegion/',
        'Titulos':Titulos,
        'Datos':datos,
        'Totales':totales,
        'Error':error,
        'MensajeError':msg,
        'FechaInicial':fechainicial,
        'FechaFinal':fechafinal,
    })
    return HttpResponse(template.render(context))

@login_required(login_url=Configuracion.LOGIN_URL)
def AjustePorMontoRegion(request,zona_id):
    template = loader.get_template(URI_TEMPLATE)
    regiones=RegionAuditoria.objects.filter(Zona__id=zona_id).order_by("NombreRegion")
    Titulos=["Registrados","Activos","Sin autorizar","Enviados","Cancelados","Procede ajuste","No Procede ajuste"]
    datos=[]
    totales=[]
    totalReg=0
    totalAct=0
    totalSinAut=0
    totalEnv=0
    totalCanc=0
    totalProc=0
    totalNoProc=0
    fechainicial=datetime.min
    fechafinal=datetime.max
    error=False
    msg=""
    if request.method == 'POST':
        datosValidacion=ValidoFechas(request)##DEVUELVE: error, msg, fechainicial, fechafinal
        error=datosValidacion[0]
        msg=datosValidacion[1]
        fechainicial=datosValidacion[2]
        fechafinal=datosValidacion[3]
    for z in regiones:
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region') \
                      .annotate(total = Sum('Monto')))
        ajuste=AjusteTipo(z.id,z.NombreRegion)
        tipo=TipoEspecifico("Registrados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalReg+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Activo=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Activos",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalAct+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Enviado=False, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Enviados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalSinAut+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Enviado=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Enviados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalEnv+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Activo=False, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region') \
                      .annotate(total = Sum('Monto')))        
        tipo=TipoEspecifico("Cancelados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalCanc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,ProcedeAjuste=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region') \
                      .annotate(total = Sum('Monto')))
        tipo=TipoEspecifico("Procede ajuste",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalProc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,NoProcedeAjuste=True, FechaRecepcion__gte=fechainicial, FechaRecepcion__lte=fechafinal)\
                      .values('Region') \
                      .annotate(total = Sum('Monto')))
        tipo=TipoEspecifico("No Procede ajuste",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalNoProc+=ajustes[0]["total"]
        
        datos.append(ajuste)
    totales.append(totalReg)
    totales.append(totalAct)
    totales.append(totalSinAut)
    totales.append(totalEnv)
    totales.append(totalCanc)
    totales.append(totalProc)
    totales.append(totalNoProc)
    if fechainicial==datetime.min:
        fechainicial=None
    if fechafinal==datetime.max:
        fechafinal=None
    context = RequestContext(request, {
        'Titulo':'Ajustes por monto por region',
        'Encabezado':'Region',
        'URL':None,
        'Titulos':Titulos,
        'Datos':datos,
        'Totales':totales,
        'Error':error,
        'MensajeError':msg,
        'FechaInicial':fechainicial,
        'FechaFinal':fechafinal,
    })
    return HttpResponse(template.render(context))

def ValidoAjustes(ajustes):    
    if ajustes.__len__()==0:        
        ajustes=[{"total":0}]
    return ajustes

def ValidoFechas(request):
    error=False
    msg=""
    fechainicial=datetime.min
    fechafinal=datetime.max
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
    if not error:        
        if type(fechainicial) is datetime and type(fechafinal) is datetime and fechainicial>=fechafinal:
            error=True
            msg ="La fecha final debe ser mayor a la fecha inicial"
    else:
        fechainicial=datetime.min
        fechafinal=datetime.max        
    return error, msg, fechainicial, fechafinal

class AjusteTipo(object):
    ID=0
    Desc=""
    Tipos=[]
    
    def __init__(self, Id, Desc):
        self.ID=Id
        self.Desc=Desc
        self.Tipos=[]
        
    def AddTipo(self, tipo):
        self.Tipos.append(tipo)

class TipoEspecifico:
    Total=0
    Desc=""
    def __init__(self, Desc, Total):
        self.Total=Total
        self.Desc=Desc
