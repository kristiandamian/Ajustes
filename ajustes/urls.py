from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from ajustesLogica.views.inicio import Inicio
from ajustesLogica.views.ajustes.controllerAjustes import AltaAjuste,RegistrarAjuste
from ajustesLogica.views.ajustes.controllerEvidencia import AltaEvidencia, AltaEvidenciaAjuste
from ajustesLogica.views.ajustes.controllerAutorizaciones import AutorizarAjustes
from ajustesLogica.views.soporte.controllerCancelaciones import CancelarAjuste
from ajustesLogica.views.soporte.controllerCorreo import ConfiguracionCorreo
from ajustesLogica.views.viewsLogin import loginUsuario, logoutUsuario
from ajustesLogica.views.ajax.Evidencias import BuscarAjustes, BuscarAjuste, upload, BuscarEvidencias
from ajustesLogica.views.ajax.Autorizaciones import RegistroAutorizacion
from ajustesLogica.views.ajax.Correos import BuscarCorreo, GrabarCorreo
from ajustesLogica.views.ajax.Cancelaciones import CanceloAjuste
from ajustesLogica.views.reportes.ControllerGraficaTendencias import TendenciasAjustes
from ajustesLogica.models import UsuarioAcceso, RegionAuditoria, ZonaAuditoria, CorreoEnviado
from ajustesLogica.models import UsuarioAccesoAdmin

############################################################################################################
admin.autodiscover()                                                                                       #
############################################################################################################
############################################################################################################
########## AGREGO AL ADMIN #################################################################################
############################################################################################################
admin.site.register(UsuarioAcceso,UsuarioAccesoAdmin)
admin.site.register(ZonaAuditoria)
admin.site.register(RegionAuditoria)
admin.site.register(CorreoEnviado)

############################################################################################################
urlpatterns = patterns('',
############################################################################################################
#### SESSION                                                                                           #####
############################################################################################################
    url(r'^ajustes/login/',loginUsuario),
    url(r'^ajustes/logout/',logoutUsuario),
############################################################################################################
#### AJUSTES DE CLIENTES                                                                                ####
############################################################################################################
    url(r'^ajustes/$',Inicio),    
    url(r'^ajustes/AltaAjuste/$',AltaAjuste),
    url(r'^ajustes/RegistrarAjuste/$',RegistrarAjuste),
    url(r'^ajustes/EvidenciaAjustes/$',AltaEvidencia),
    url(r'^ajustes/EvidenciaAjustes/(?P<ajuste>\d+)/',AltaEvidenciaAjuste),    
    url(r'^ajustes/AutorizarAjustes/$',AutorizarAjustes),    
############################################################################################################
#### AJAX                                                                                               ####
############################################################################################################
    url(r'^ajustes/ajax/BuscarAjustes/$',BuscarAjustes),
    url(r'^ajustes/ajax/BuscarAjuste/$',BuscarAjuste),
    url(r'^ajustes/ajax/RegistroAutorizacion/$',RegistroAutorizacion),
    url(r'^ajustes/ajax/upload/$',upload),
    url(r'^ajustes/ajax/BuscarEvidencias/$',BuscarEvidencias),
    url(r'^ajustes/ajax/BuscarCorreo/$',BuscarCorreo),
    url(r'^ajustes/ajax/GrabarCorreo/$',GrabarCorreo),
    url(r'^ajustes/ajax/CanceloAjuste/$',CanceloAjuste),
############################################################################################################
####    SOPORTE                                                                                         ####
############################################################################################################   
    #url(r'^ajustes/ReenviarCorreo/$',ReenviarCorreo),    
    url(r'^ajustes/ConfiguracionCorreo/$',ConfiguracionCorreo),
    url(r'^ajustes/CancelarAjustes/$',CancelarAjuste),
    
############################################################################################################
####    REPORTES                                                                                        ####
############################################################################################################   
    url(r'^ajustes/GraficaTendenciasAjustes/$',TendenciasAjustes),
############################################################################################################
####  LIGA PARA LOS ARCHIVOS SUBIDOS (EVIDENCIAS)                                                      ####
############################################################################################################    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

############################################################################################################
####                             ADMIN                                                                  ####
############################################################################################################
    url(r'^ajustes/admin/', include(admin.site.urls)),
) 

