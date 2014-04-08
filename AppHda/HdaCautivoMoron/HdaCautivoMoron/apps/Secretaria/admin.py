# -*- coding: utf-8 -*- 
from django.contrib import admin
from HdaCautivoMoron.apps.Secretaria.models import Entidad, HermanoDeAlta, HermanoDeBaja

"""
#PERSONALIZAR UNA LISTA DE MODIFICACIONES
	search_fields = ('usuario',)
	list_display = ('titulo','editores','fecha_publicacion')
	list_filter = ('autores','fecha_publicacion')
	date_hierarchy = 'fecha_publicacion'
	ordering = ('-fecha_publicacion',)
	
#PERSONALIZAR FORMULARIOS DE EDICION
	fields = ('titulo','autores','editores','fecha_publicacion')

	#*-* MUCHOS A MUCHOS
	filter_horizontal = ('autores',)	
	filter_vertical = ('autores',)	

	#1-* UNO A MUCHOS
	raw_id_fields = ('editores',)
"""

class HermanoDeAltaAdmin(admin.ModelAdmin):
	search_fields = ('nombre','apellidos',)
	list_display = ('numHermano','nombre','apellidos', 'dni', 'telefono','email',)
	list_filter = ('formaDePago','activo',)
	ordering = ('numHermano',)


class HermanoDeBajaAdmin(admin.ModelAdmin):
	search_fields = ('hermano__nombre','hermano__apellidos',)
	list_display = ('hermano_nombre','hermano_apellidos','motivo','fechaBaja')
	ordering = ('fechaBaja',)
	list_filter = ('motivo',)
	raw_id_fields = ('hermano',)

	def hermano_nombre(self,instance):
		return instance.hermano.nombre

	def hermano_apellidos(self,instance):
		return instance.hermano.apellidos


class EntidadAdmin(admin.ModelAdmin):
	list_display = ('apodo','telefono','email',)
	list_filter = ('estado',)
	ordering = ('apodo',)



admin.site.register(HermanoDeAlta,HermanoDeAltaAdmin)
admin.site.register(HermanoDeBaja,HermanoDeBajaAdmin)
admin.site.register(Entidad,EntidadAdmin)
