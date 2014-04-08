# -*- coding: utf-8 -*- 
from django.contrib import admin
from HdaCautivoMoron.apps.DipMayorDeGobierno.models import Paso, Tramo, SubTramo, Insignia, Elemento, Cuadrilla, HermanoLLevaInsignia, HermanoLLevaElemento, HermanoCuadrilla, Tunica, tunicaAlquilerDelHermano

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

class TramoAdmin(admin.ModelAdmin):
	list_display = ('nombre','paso_tramo',)
	ordering =('nombre',)

	def paso_tramo(self, instance):
		return instance.pasoAlQuePertenece.nombre



class SubTramoAdmin(admin.ModelAdmin):
	list_display = ('nombre','tramo_nombre','tramo_paso',)
	ordering = ('tramoAlQuePertenece__nombre','nombre',)

	def tramo_nombre(self, instance):
		return instance.tramoAlQuePertenece.nombre
	def tramo_paso(self, instance):
		return instance.tramoAlQuePertenece.pasoAlQuePertenece.nombre



class InsigniaAdmin(admin.ModelAdmin):
	search_fields = ('nombre',)
	list_display = ('nombre','orden', 'precio', 'cantidad', 'tramo_nombre',)
	list_filter = ('tramoAlQuePertenece__nombre',)
	ordering = ('tramoAlQuePertenece__nombre', 'orden',)

	
	def tramo_nombre(self, instance):
		return instance.tramoAlQuePertenece.nombre



class ElementoAdmin(admin.ModelAdmin):
	list_display = ('nombre','tipo', 'elemento_paso', 'precio',)
	ordering = ('pasoAlQuePertenece__nombre', 'nombre',)

	def elemento_paso(self, instance):
		return instance.pasoAlQuePertenece.nombre




class HermanoLLevaInsigniaAdmin(admin.ModelAdmin):
	search_fields = ('hermano__nombre','hermano__apellidos',)
	raw_id_fields =('hermano','insignia',)
	list_display = ('hermano_nombre','insignia_nombre', 'fecha_anyo',)
	list_filter = ('insignia__nombre','fecha',)
	date_hierarchy = 'fecha'


	def hermano_nombre(self, instance):
		return u'%s, %s'%(instance.hermano.apellidos, instance.hermano.nombre)
	def insignia_nombre(self, instance):
		return instance.insignia.nombre
	def fecha_anyo(self, instance):
		return instance.fecha.year



class HermanoLLevaElementoAdmin(admin.ModelAdmin):
	raw_id_fields=('hermano', 'elemento',)
	search_fields = ('hermano__nombre','hermano__apellidos')
	list_display = ('hermano_nombre','elemento_nombre', 'fecha_anyo', 'idTramo', 'numPareja')
	list_filter = ('elemento__pasoAlQuePertenece__nombre','fecha')
	ordering = ('fecha',)
	date_hierarchy = 'fecha'

	def hermano_nombre(self, instance):
		return u'%s, %s'%(instance.hermano.apellidos, instance.hermano.nombre)
	def elemento_nombre(self, instance):		
		return instance.elemento.nombre
	def fecha_anyo(self, instance):
		return instance.fecha.year

class HermanoCuadrillaAdmin(admin.ModelAdmin):
	list_display = ('hermano_nombre','cuadrilla_nombre','fecha_anyo',)
	search_fields = ('hermano__nombre','hermano__apellidos')
	list_filter = ('cuadrilla__nombre','fecha',)
	ordering = ('fecha',)
	date_hierarchy = 'fecha'
	raw_id_fields = ('hermano','cuadrilla',)

	def hermano_nombre(self, instance):
		return u'%s, %s'%(instance.hermano.apellidos, instance.hermano.nombre)
	def cuadrilla_nombre(self, instance):
		return instance.cuadrilla.nombre
	def fecha_anyo(self, instance):
		return instance.fecha.year

	



class TunicaAdmin(admin.ModelAdmin):
	list_display = ('tipo', 'precio')


class tunicaAlquilerDelHermanoAdmin(admin.ModelAdmin):
	search_fields = ('hermano__nombre','hermano__apellidos',)
	raw_id_fields = ('hermano', 'tunica')
	list_display = ('hermano_nombre', 'tunica_nombre','devuelta', 'fecha_anyo',)
	list_filter = ('devuelta', 'fecha',)
	date_hierarchy = 'fecha'

	def hermano_nombre(self, instance):
		return u'%s, %s'%(instance.hermano.apellidos, instance.hermano.nombre)
	def tunica_nombre(self, instance):
		return instance.tunica.tipo
	def fecha_anyo(self, instance):
		return instance.fecha.year

admin.site.register(Paso)
admin.site.register(Tramo, TramoAdmin)
admin.site.register(SubTramo, SubTramoAdmin)
admin.site.register(Insignia, InsigniaAdmin)
admin.site.register(Elemento, ElementoAdmin)
admin.site.register(Cuadrilla)
admin.site.register(HermanoLLevaInsignia, HermanoLLevaInsigniaAdmin)
admin.site.register(HermanoLLevaElemento, HermanoLLevaElementoAdmin)
admin.site.register(HermanoCuadrilla,HermanoCuadrillaAdmin)
admin.site.register(Tunica,TunicaAdmin)
admin.site.register(tunicaAlquilerDelHermano, tunicaAlquilerDelHermanoAdmin)
