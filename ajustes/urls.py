from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from ajustesLogica.views.inicio import Inicio
from ajustesLogica.views.ajustes.controllerAjustes import AltaAjuste,RegistrarAjuste, VerAjustes, VerAjuste
from ajustesLogica.views.ajustes.controllerEvidencia import AltaEvidencia, AltaEvidenciaAjuste
from ajustesLogica.views.ajustes.controllerAutorizaciones import AutorizarAjustes
from ajustesLogica.views.ajustes.controllerCierre import FinalizarAjuste
from ajustesLogica.views.soporte.controllerCancelaciones import CancelarAjuste
from ajustesLogica.views.soporte.controllerCorreo import ConfiguracionCorreo
from ajustesLogica.views.viewsLogin import loginUsuario, logoutUsuario
from ajustesLogica.views.ajax.Ajustes import BuscarTodosLosAjustes, BuscarNotasAjuste
from ajustesLogica.views.ajax.Evidencias import BuscarAjustes, BuscarAjuste, upload, BuscarEvidencias
from ajustesLogica.views.ajax.Autorizaciones import RegistroAutorizacion
from ajustesLogica.views.ajax.Correos import BuscarCorreo, GrabarCorreo
from ajustesLogica.views.ajax.Cancelaciones import CanceloAjuste
from ajustesLogica.views.ajax.Finalizaciones import FinalizacionAjuste
from ajustesLogica.views.ajax.SA import BuscarSAs, GrabarSAs
from ajustesLogica.views.reportes.controllerGraficaTendencias import TendenciasAjustes
from ajustesLogica.views.reportes.controllerAjustesPorFecha import AjustesPorFecha
from ajustesLogica.views.reportes.controllerAjustePorTipo import AjustePorTipoZona, AjustePorTipoRegion
from ajustesLogica.views.reportes.controllerAjustePorMonto import AjustePorMontoZona, AjustePorMontoRegion
from ajustesLogica.views.reportes.controllerAjustePorClasificacionZona import AjustePorClasificacionZona, AjustePorClasificacionRegion
from ajustesLogica.views.reportes.controllerDistribucionClasificaciones import DistribucionClasificacion
from ajustesLogica.views.reportes.controllerDistribucionEstatus import DistribucionEstatus
from ajustesLogica.views.reportes.controllerDistribucionCentros import DistribucionCentro
from ajustesLogica.views.reportes.controllerAjustesSinEvidencia import AjusteSinEvidencia
from ajustesLogica.views.reportes.controllerAjustesCancelados import AjustesCancelados
from ajustesLogica.views.SeguimientoSA.controllerSA import SeguimientoSA
from ajustesLogica.models import UsuarioAcceso, RegionAuditoria, ZonaAuditoria, ClasificacionAjuste
from ajustesLogica.models import UsuarioAccesoAdmin

############################################################################################################
admin.autodiscover()                                                                                    ####
############################################################################################################
############################################################################################################
########## AGREGO AL ADMIN #################################################################################
############################################################################################################
############################################################################################################
admin.site.register(UsuarioAcceso,UsuarioAccesoAdmin)                                                   ####
admin.site.register(ZonaAuditoria)                                                                      ####
admin.site.register(RegionAuditoria)                                                                    ####
admin.site.register(ClasificacionAjuste)                                                                ####
############################################################################################################
urlpatterns = patterns('',                                                                              ####
############################################################################################################
#### SESSION                                                                                           #####
############################################################################################################
    url(r'^ajustes/login/',loginUsuario),                                                               ####
    url(r'^ajustes/logout/',logoutUsuario),                                                             ####
############################################################################################################
#### AJUSTES DE CLIENTES                                                                                ####
############################################################################################################
    url(r'^ajustes/$',AjustePorTipoZona),                                                               ####
    url(r'^ajustes/AltaAjuste/$',AltaAjuste),                                                           ####
    url(r'^ajustes/Ajuste/$',VerAjustes),                                                               ####
    url(r'^ajustes/Ajuste/(?P<ajuste>\d+)/$',VerAjuste),                                                ####
    url(r'^ajustes/RegistrarAjuste/$',RegistrarAjuste),                                                 ####
    url(r'^ajustes/EvidenciaAjustes/$',AltaEvidencia),                                                  ####
    url(r'^ajustes/EvidenciaAjustes/(?P<ajuste>\d+)/',AltaEvidenciaAjuste),                             ####
    url(r'^ajustes/AutorizarAjustes/$',AutorizarAjustes),                                               ####
    url(r'^ajustes/FinalizarAjuste/$',FinalizarAjuste),                                                 ####
############################################################################################################
#### MANEJO DE S.A. ENVIADAS                                                                            ####
############################################################################################################
    url(r'^ajustes/SeguimientoSA/$',SeguimientoSA),                                                     ####
############################################################################################################
#### AJAX                                                                                               ####
############################################################################################################
    url(r'^ajustes/ajax/BuscarAjustes/$',BuscarAjustes),                                                ####
    url(r'^ajustes/ajax/BuscarAjuste/$',BuscarAjuste),                                                  ####
    url(r'^ajustes/ajax/BuscarTodosLosAjustes/$',BuscarTodosLosAjustes),                                ####
    url(r'^ajustes/ajax/BuscarDatosAjuste/$',BuscarNotasAjuste),                                        ####
    url(r'^ajustes/ajax/RegistroAutorizacion/$',RegistroAutorizacion),                                  ####
    url(r'^ajustes/ajax/upload/$',upload),                                                              ####
    url(r'^ajustes/ajax/BuscarEvidencias/$',BuscarEvidencias),                                          ####
    url(r'^ajustes/ajax/BuscarCorreo/$',BuscarCorreo),                                                  ####
    url(r'^ajustes/ajax/GrabarCorreo/$',GrabarCorreo),                                                  ####
    url(r'^ajustes/ajax/CanceloAjuste/$',CanceloAjuste),                                                ####
    url(r'^ajustes/ajax/FinalizarAjuste/$',FinalizacionAjuste),                                         ####
    url(r'^ajustes/ajax/BuscarSAs/$',BuscarSAs),                                                        ####
    url(r'^ajustes/ajax/GrabarSA/$',GrabarSAs),                                                         ####
############################################################################################################
####    SOPORTE                                                                                         ####
############################################################################################################
    url(r'^ajustes/ConfiguracionCorreo/$',ConfiguracionCorreo),                                         ####
    url(r'^ajustes/CancelarAjustes/$',CancelarAjuste),                                                  ####
############################################################################################################
####    REPORTES                                                                                        ####
############################################################################################################
    url(r'^ajustes/GraficaTendenciasAjustes/$',TendenciasAjustes),                                      ####
    url(r'^ajustes/AjustesPorFecha/$',AjustesPorFecha),                                                 ####
    url(r'^ajustes/AjustesSinEvidencia/$',AjusteSinEvidencia),                                          ####
    url(r'^ajustes/AjustePorTipoZona/$',AjustePorTipoZona),                                             ####
    url(r'^ajustes/AjustePorTipoRegion/(?P<zona_id>\d+)/$',AjustePorTipoRegion),                        ####
    url(r'^ajustes/AjustePorMontoZona/$',AjustePorMontoZona),                                           ####
    url(r'^ajustes/AjustePorMontoRegion/(?P<zona_id>\d+)/$',AjustePorMontoRegion),                      ####
    url(r'^ajustes/AjustePorClasificacionZona/$',AjustePorClasificacionZona),                           ####
    url(r'^ajustes/AjustePorClasificacionRegion/(?P<zona_id>\d+)/$',AjustePorClasificacionRegion),      ####
    url(r'^ajustes/DistribucionClasificacion/$',DistribucionClasificacion),                             ####
    url(r'^ajustes/DistribucionEstatus/$',DistribucionEstatus),                                         ####
    url(r'^ajustes/DistribucionCentro/$',DistribucionCentro),                                           ####
    url(r'^ajustes/AjustesCancelados/$',AjustesCancelados),                                             ####    
############################################################################################################
####  LIGA PARA LOS ARCHIVOS SUBIDOS (EVIDENCIAS)                                                       ####
############################################################################################################
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),     ####
############################################################################################################
####                             ADMIN                                                                  ####
############################################################################################################
    url(r'^ajustes/admin/', include(admin.site.urls)),                                                  ####
)                                                                                                       ####
############################################################################################################