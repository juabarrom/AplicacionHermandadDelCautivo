from django.conf.urls import patterns, include, url

urlpatterns = patterns('HdaCautivoMoron.apps.Secretaria.views',
	url(r'^indice/$', 'indice_view', name='vista_principal'),

	url(r'^Secretaria/datosHermano/(?P<idHermano>.*)/$', 'datosHermano_view', name='vista_datosHermano'),

)
