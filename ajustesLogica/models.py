#!/usr/bin/env python
import sys
from django.db import models
from django.forms import ModelForm, DateInput
from django.contrib import admin
from django.contrib.auth.models import User

class ZonaAuditoriaManager(models.Manager):
    def PorPermiso(self, user):
        usuario=UsuarioAcceso.objects.filter(Usuario=user)
        if usuario.__len__()==0 or  user.is_superuser or usuario[0].Region==None:#no hay un usuario o ese usuario es "superusuario" o tiene acceso a nivel nacional
           return super(ZonaAuditoriaManager,self).get_query_set()
        zonas=[]
        for u in usuario:                          
            if u.Zona!=None:
                zonas+=ZonaAuditoria.objects.filter(id=u.Zona.id).values_list("id",flat=True)
            else:
                if u.Region!=None:
                    zonas+=RegionAuditoria.objects.filter(Zona__id=u.Zona.id).values_list("Zona__id",flat=True)
        return super(ZonaAuditoriaManager,self).get_query_set().filter(id__in = zonas)
    
class ZonaAuditoria(models.Model):
    NombreZona=models.CharField(max_length=1000)
    GerenteZona=models.CharField(max_length=1000)
    Correo=models.EmailField(max_length=100)
    
    objects=ZonaAuditoriaManager()
    
    def __unicode__(self):
        return self.NombreZona+"-"+self.GerenteZona
    class Meta:        
        ordering =['NombreZona']
        
class RegionAuditoriaManager(models.Manager):
    def PorPermiso(self, user):
        usuario=UsuarioAcceso.objects.filter(Usuario=user)
        if usuario.__len__()==0 or  user.is_superuser or usuario[0].Region==None:#no hay un usuario o ese usuario es "superusuario" o tiene acceso a nivel nacional
           return super(RegionAuditoriaManager,self).get_query_set()
        regiones=[]
        for u in usuario:                          
            if u.Zona!=None and u.Region!=None:
                regiones+=RegionAuditoria.objects.filter(id=u.Region.id).values_list("id",flat=True)
            else:
                if u.Zona!=None:                
                    regiones+=RegionAuditoria.objects.filter(Zona__id=u.Zona.id).values_list("id",flat=True)            
        return super(RegionAuditoriaManager,self).get_query_set().filter(id__in = regiones)
    
class RegionAuditoria(models.Model):
    NombreRegion=models.CharField(max_length=1000)
    GerenteRegion=models.CharField(max_length=1000)
    Zona=models.ForeignKey(ZonaAuditoria)
    Correo=models.EmailField(max_length=100)
    Password=models.CharField(max_length=1000, blank=True, null=True)
    
    objects=RegionAuditoriaManager()
    
    def __unicode__(self):
        return self.NombreRegion + "-" + self.GerenteRegion
    
    class Meta:        
        ordering =['NombreRegion']

class Ajuste(models.Model):
    Region = models.ForeignKey(RegionAuditoria)
    FechaRecepcion=models.DateField()
    NumEnvioMensajeria = models.CharField('Envio de mensajeria',max_length=200)
    Tienda = models.IntegerField('Tienda que manda ajustar')
    NumEmpleado = models.IntegerField('Num. Empleado que manda ajustar')    
    NomEmpleado = models.CharField('Nombre del empleado que manda ajustar',max_length=200)
    NumCte = models.IntegerField('Num. de cliente')
    NumCuentas = models.IntegerField('Num. de cuentas a ajustar')
    Monto=models.DecimalField(verbose_name='Monto del ajuste',default=0, max_digits=18,decimal_places=2)
    Activo=models.BooleanField(verbose_name='Estatus', default=True)
    ProcedeAjuste=models.BooleanField(verbose_name='Procede ajuste', blank=True)
    NoProcedeAjuste=models.BooleanField(verbose_name='Procede ajuste', blank=True)
    FechaRegistroSistema=models.DateTimeField(auto_now=True)
    Enviado=models.BooleanField(verbose_name='Enviado a cobranza ajuste', default=False)
    Finalizado=models.BooleanField(default=False)
    Usuario=models.ForeignKey(User)
    
    class Meta:
        permissions = (
            ("Puede_Cancelar", "Puede cancelar ajustes"),
        )

class ClasificacionAjuste(models.Model):    
    Clasificacion=models.CharField(max_length=1000)
    Descripcion=models.CharField(max_length=10000)
    
    def __unicode__(self):
        return u'%s' % (self.Clasificacion)
    
class CuentaAfectadaAjuste(models.Model):
    TIPO_CENTRO=(
        (1,'Muebles'),
        (2,'Ropa'),
        (3,'Cajas'),
        (4,'Tiempo Aire'),
        (5,'Coppel.com'),
        (6,'Negocios afiliados')
    )
    AjusteAfectado=models.ForeignKey(Ajuste)
    Tipo=models.IntegerField(choices=TIPO_CENTRO)
    Factura=models.IntegerField()
    Tienda=models.IntegerField(verbose_name='Tda. donde se facturo')
    Fecha=models.DateField(verbose_name='Fecha de la factura')
    Monto=models.DecimalField(verbose_name='Monto de la factura',default=0, max_digits=18,decimal_places=2)

class CuentaAfectadaAjusteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CuentaAfectadaAjusteForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'El campo es requerido.'
    class Meta:
        model=CuentaAfectadaAjuste
        widgets  = {
            'Fecha': DateInput(attrs={'class':'datepicker'}),
        }
        exclude=('AjusteAfectado')

class CierreAjuste(models.Model):
    TIPO_ESTATUS=(
        (1,'Recuperable'),
        (2,'No Recuperable'),
        (3,'Aclarado con soporte'),
    )
    AjusteAfectado=models.ForeignKey(Ajuste)
    Clasificacion=models.ForeignKey(ClasificacionAjuste)
    Observaciones = models.CharField(max_length=5000)
    Estatus=models.IntegerField(choices=TIPO_ESTATUS)    
    FechaRegistroSistema=models.DateTimeField(auto_now=True)
    Usuario=models.ForeignKey(User)

class EmpleadosResponsables(models.Model):
    TIPO_ESTATUS_LABORAL=(
        (1,'Activo en nomina'),
        (2,'Baja'),
    )
    Cierre= models.ForeignKey(CierreAjuste)
    NumEmpleado = models.IntegerField('Num. Empleado que manda ajustar')
    NomEmpleado = models.CharField('Nombre del empleado que manda ajustar',max_length=200)
    EstatusLaboral=models.IntegerField(choices=TIPO_ESTATUS_LABORAL)
    
class AjusteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AjusteForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'El campo es requerido.'
    class Meta:
        model=Ajuste
        widgets  = {
            'FechaRecepcion': DateInput(attrs={'class':'datepicker'}),
        }
        exclude=('FechaRegistroSistema','Usuario','ProcedeAjuste','NoProcedeAjuste','Activo','Enviado','Finalizado')

class ImagenAjuste(models.Model):
    Imagen = models.CharField('Imagen',max_length=500)
    archivo = models.FileField(upload_to='uploads/%Y/%m/%d')
    CorrespondeAjuste=models.ForeignKey(Ajuste)
    Activo=models.BooleanField(verbose_name='Procede ajuste', default=True)
    FechaRegistroSistema=models.DateTimeField(auto_now=True)
    Usuario=models.ForeignKey(User)
    
    def __unicode__(self):
        return u'%s' % (self.Imagen)

class Autorizacion(models.Model):
    FechaRegistroSistema=models.DateTimeField(auto_now=True)
    Usuario=models.ForeignKey(User)
    AjusteAutorizado=models.ForeignKey(Ajuste)
    
    class Meta:
        permissions = (
            ("Puede_Autorizar", "Puede autorizar ajustes"),
        )
    
class UsuarioAcceso(models.Model):
    Usuario=models.ForeignKey(User)
    Region=models.ForeignKey(RegionAuditoria, null=True, blank=True)
    Zona=models.ForeignKey(ZonaAuditoria, null=True, blank=True)
    
    def __unicode__(self):
        if self.Region!=None:
            return self.Usuario.username +"-"+ self.Region.NombreRegion
        else:
            return self.Usuario.username
    
    class Meta:
        verbose_name_plural='UsuariosAccesos'
        ordering =['Zona__NombreZona']        
        
class UsuarioAccesoAdmin(admin.ModelAdmin):
    list_filter =('Zona__NombreZona',)
    search_fields =['Usuario__username','Zona__NombreZona','Region__NombreRegion']
    
class SeguimientoSA(models.Model):
    AjusteAfectado=models.ForeignKey(Ajuste)
    Folio=models.CharField(max_length=500)
    Destinatario=models.CharField(max_length=500)
    Puesto=models.CharField(max_length=500)
    Tema=models.CharField(max_length=5000)
    Fecha=models.DateField()
    