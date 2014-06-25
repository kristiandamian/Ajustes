from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.db.models import Count
from ajustesLogica.models import RegionAuditoria, Ajuste, ZonaAuditoria
from ajustesLogica.Config import Configuracion

@login_required(login_url=Configuracion.LOGIN_URL)
def AjustePorTipoZona(request):
    template = loader.get_template('reportes/AjustesPorTipo.html')
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
    for z in zonas:
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z)\
                      .values('Region__Zona') \
                      .annotate(total = Count('Tienda')))
        ajuste=AjusteTipo(z.id,z.NombreZona)
        tipo=TipoEspecifico("Registrados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalReg+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Activo=True)\
                      .values('Region__Zona') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Activos",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalAct+=ajustes[0]["total"]

        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Enviado=False)\
                      .values('Region__Zona') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Sin autorizar",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalSinAut+=ajustes[0]["total"]

        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Enviado=True)\
                      .values('Region__Zona') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Enviados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalEnv+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,Activo=False)\
                      .values('Region__Zona') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Cancelados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalCanc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,ProcedeAjuste=True)\
                      .values('Region__Zona') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Procede ajuste",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalProc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region__Zona=z,NoProcedeAjuste=True)\
                      .values('Region__Zona') \
                      .annotate(total = Count('Tienda')))        
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
    
    context = RequestContext(request, {
        'Titulo':'Ajustes por tipo por zona',        
        'Encabezado':'Zona',
        'URL':'/ajustes/AjustePorTipoRegion/',
        'Titulos':Titulos,
        'Datos':datos,
        'Totales':totales,
    })
    return HttpResponse(template.render(context))

@login_required(login_url=Configuracion.LOGIN_URL)
def AjustePorTipoRegion(request,zona_id):
    template = loader.get_template('reportes/AjustesPorTipo.html')
    regiones=RegionAuditoria.objects.PorPermiso(request.user)
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
    for z in regiones:
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z)\
                      .values('Region') \
                      .annotate(total = Count('Tienda')))
        ajuste=AjusteTipo(z.id,z.NombreRegion)
        tipo=TipoEspecifico("Registrados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalReg+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Activo=True)\
                      .values('Region') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Activos",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalAct+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Enviado=False)\
                      .values('Region') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Enviados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalSinAut+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Enviado=True)\
                      .values('Region') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Enviados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalEnv+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,Activo=False)\
                      .values('Region') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Cancelados",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalCanc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,ProcedeAjuste=True)\
                      .values('Region') \
                      .annotate(total = Count('Tienda')))        
        tipo=TipoEspecifico("Procede ajuste",ajustes[0]["total"])
        ajuste.AddTipo(tipo)
        
        totalProc+=ajustes[0]["total"]
        
        ajustes=ValidoAjustes(Ajuste.objects.filter(Region=z,NoProcedeAjuste=True)\
                      .values('Region') \
                      .annotate(total = Count('Tienda')))        
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
    
    context = RequestContext(request, {
        'Titulo':'Ajustes por tipo por region',        
        'Encabezado':'Region',
        'URL':None,
        'Titulos':Titulos,
        'Datos':datos,
        'Totales':totales,
    })
    return HttpResponse(template.render(context))

def ValidoAjustes(ajustes):    
    if ajustes.__len__()==0:        
        ajustes=[{"total":0}]
    return ajustes

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
