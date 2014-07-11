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
from ajustesLogica.views.ajax.Ajustes import BuscarTodosLosAjustes, BuscarNotasAjuste, BuscarAjustePorCte
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
from ajustesLogica.views.reportes.controllerDistribucionTiendas import DistribucionTienda
from ajustesLogica.views.reportes.controllerAjustePorFraudeZona import AjustePorFraudeZona, AjustePorFraudeRegion
from ajustesLogica.views.reportes.controllerAjustesSinFinalizar import AjustesSinFinalizar
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
patronURI='ajustes/'
############################################################################################################
urlpatterns = patterns('',                                                                              ####
############################################################################################################
#### SESSION                                                                                           #####
############################################################################################################
    url(r'^'+patronURI+'login/',loginUsuario),                                                          ####
    url(r'^'+patronURI+'logout/',logoutUsuario),                                                        ####
############################################################################################################
#### AJUSTES DE CLIENTES                                                                                ####
############################################################################################################
    url(r'^'+patronURI+'$',AjustePorTipoZona),                                                          ####
    url(r'^'+patronURI+'AltaAjuste/$',AltaAjuste),                                                      ####
    url(r'^'+patronURI+'Ajuste/$',VerAjustes),                                                          ####
    url(r'^'+patronURI+'Ajuste/(?P<ajuste>\d+)/$',VerAjuste),                                           ####
    url(r'^'+patronURI+'RegistrarAjuste/$',RegistrarAjuste),                                            ####
    url(r'^'+patronURI+'EvidenciaAjustes/$',AltaEvidencia),                                             ####
    url(r'^'+patronURI+'EvidenciaAjustes/(?P<ajuste>\d+)/',AltaEvidenciaAjuste),                        ####
    url(r'^'+patronURI+'AutorizarAjustes/$',AutorizarAjustes),                                          ####
    url(r'^'+patronURI+'FinalizarAjuste/$',FinalizarAjuste),                                            ####
############################################################################################################
#### MANEJO DE S.A. ENVIADAS                                                                            ####
############################################################################################################
    url(r'^'+patronURI+'SeguimientoSA/$',SeguimientoSA),                                                ####
############################################################################################################
#### AJAX                                                                                               ####
############################################################################################################
    url(r'^'+patronURI+'ajax/BuscarAjustes/$',BuscarAjustes),                                           ####
    url(r'^'+patronURI+'ajax/BuscarAjuste/$',BuscarAjuste),                                             ####
    url(r'^'+patronURI+'ajax/BuscarTodosLosAjustes/$',BuscarTodosLosAjustes),                           ####
    url(r'^'+patronURI+'ajax/BuscarDatosAjuste/$',BuscarNotasAjuste),                                   ####
    url(r'^'+patronURI+'ajax/RegistroAutorizacion/$',RegistroAutorizacion),                             ####
    url(r'^'+patronURI+'ajax/upload/$',upload),                                                         ####
    url(r'^'+patronURI+'ajax/BuscarEvidencias/$',BuscarEvidencias),                                     ####
    url(r'^'+patronURI+'ajax/BuscarCorreo/$',BuscarCorreo),                                             ####
    url(r'^'+patronURI+'ajax/GrabarCorreo/$',GrabarCorreo),                                             ####
    url(r'^'+patronURI+'ajax/CanceloAjuste/$',CanceloAjuste),                                           ####
    url(r'^'+patronURI+'ajax/FinalizarAjuste/$',FinalizacionAjuste),                                    ####
    url(r'^'+patronURI+'ajax/BuscarSAs/$',BuscarSAs),                                                   ####
    url(r'^'+patronURI+'ajax/GrabarSA/$',GrabarSAs),                                                    ####
    url(r'^'+patronURI+'ajax/BuscarAjustePorCte/$',BuscarAjustePorCte),                                 ####
############################################################################################################
####    SOPORTE                                                                                         ####
############################################################################################################
    url(r'^'+patronURI+'ConfiguracionCorreo/$',ConfiguracionCorreo),                                    ####
    url(r'^'+patronURI+'CancelarAjustes/$',CancelarAjuste),                                             ####
############################################################################################################
####    REPORTES                                                                                        ####
############################################################################################################
    url(r'^'+patronURI+'GraficaTendenciasAjustes/$',TendenciasAjustes),                                 ####
    url(r'^'+patronURI+'AjustesPorFecha/$',AjustesPorFecha),                                            ####
    url(r'^'+patronURI+'AjustesSinEvidencia/$',AjusteSinEvidencia),                                     ####
    url(r'^'+patronURI+'AjustePorTipoZona/$',AjustePorTipoZona),                                        ####
    url(r'^'+patronURI+'AjustePorTipoRegion/(?P<zona_id>\d+)/$',AjustePorTipoRegion),                   ####
    url(r'^'+patronURI+'AjustePorMontoZona/$',AjustePorMontoZona),                                      ####
    url(r'^'+patronURI+'AjustePorMontoRegion/(?P<zona_id>\d+)/$',AjustePorMontoRegion),                 ####
    url(r'^'+patronURI+'AjustePorClasificacionZona/$',AjustePorClasificacionZona),                      ####
    url(r'^'+patronURI+'AjustePorClasificacionRegion/(?P<zona_id>\d+)/$',AjustePorClasificacionRegion), ####
    url(r'^'+patronURI+'DistribucionClasificacion/$',DistribucionClasificacion),                        ####
    url(r'^'+patronURI+'DistribucionEstatus/$',DistribucionEstatus),                                    ####
    url(r'^'+patronURI+'DistribucionCentro/$',DistribucionCentro),                                      ####
    url(r'^'+patronURI+'AjustesCancelados/$',AjustesCancelados),                                        ####
    url(r'^'+patronURI+'DistribucionTienda/$',DistribucionTienda),                                      ####
    url(r'^'+patronURI+'AjustePorFraude/$',AjustePorFraudeZona),                                        ####
    url(r'^'+patronURI+'AjustePorFraudeRegion/(?P<zona_id>\d+)/$',AjustePorFraudeRegion),               ####
    url(r'^'+patronURI+'AjustesSinFinalizar/$',AjustesSinFinalizar),                                    ####
############################################################################################################
####  LIGA PARA LOS ARCHIVOS SUBIDOS (EVIDENCIAS)                                                       ####
############################################################################################################
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),     ####
############################################################################################################
####                             ADMIN                                                                  ####
############################################################################################################
    url(r'^'+patronURI+'admin/', include(admin.site.urls)),                                             ####
)                                                                                                       ####
############################################################################################################