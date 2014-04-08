from django.conf.urls import patterns, include, url

urlpatterns = patterns('HdaCautivoMoron.apps.DipMayorDeGobierno.views',
	url(r'^dipMayorDeGobierno/$', 'indicedipMayorDeGobierno_view', name='vista_principal_dipMayorDeGobierno'),
	url(r'^dipMayorDeGobierno/historialDeLaCofradia/$', 'historialDeLaCofradia_view', name='vista_historialDeLaCofradia'),
	

	url(r'^dipMayorDeGobierno/mostrarCoincidencias/(?P<pagina>.*)/$', 'mostrarCoincidencia_view', name='vista_mostrarCoincidencia'),
	url(r'^dipMayorDeGobierno/papeltaDeSitio/(?P<idHermano>.*)/$', 'papeletaDeSitio_view', name='vista_papeletaDeSitio'),

	url(r'^dipMayorDeGobierno/insignia/(?P<idHermano>.*)/$', 'papeletaDeSitioInsignia_view', name='vista_papeletaDeSitioInsignia'),
	url(r'^dipMayorDeGobierno/luces/(?P<idHermano>.*)/$', 'papeletaDeSitioLuces_view', name='vista_papeletaDeSitioLuces'),
	url(r'^dipMayorDeGobierno/cuadrilla/(?P<idHermano>.*)/$', 'papeletaDeSitioCuadrilla_view', name='vista_papeletaDeSitioCuadrilla'),


)
