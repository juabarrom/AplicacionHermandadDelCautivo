# -*- coding: utf-8 -*- 
from django.db import models, connection
from HdaCautivoMoron.apps.Secretaria.models import HermanoDeAlta


#########################################################################################################################################
#####		INVENTARIO DE INSIGNIAS, ORDEN DE LOS TRAMOS EN LA COFRADIA, INSIGNIAS QUE PERTENECEN A UN TRAMO y OTROS ELEMENTOS		#####
#########################################################################################################################################

NOMBRE_CHOICE = (
	('CAUTIVO','PASO CRISTO'),
	('PAZ','PASO VIRGEN'),
)
class Paso(models.Model):
	nombre = models.CharField (max_length=8, choices=NOMBRE_CHOICE)
	nombreImagen = models.CharField (max_length=30)
	numOrden = models.IntegerField()

	class Meta:
		db_table = "paso"
		verbose_name = "Paso"
		

	def __unicode__(self):
	    	return self.nombreImagen


class Tramo(models.Model):
	pasoAlQuePertenece = models.ForeignKey(Paso, related_name="Paso al que pertenece el tramo", db_column="id_Paso")
	nombre = models.CharField (max_length=100)
	numOrden = models.IntegerField()

	class Meta:
		db_table = "tramo"
		verbose_name = "Tramo"
		

	def __unicode__(self):
	    	return self.nombre


class SubTramo(models.Model):
	tramoAlQuePertenece = models.ForeignKey(Tramo, related_name="Tramo al que pertenece la insignia", db_column="id_Tramo")
	nombre = models.CharField (max_length=100)
	numOrden = models.IntegerField()

	class Meta:
		db_table = "subTramo"
		verbose_name = "SubTramo"
		

	def __unicode__(self):
	    	return self.nombre


#########################################
#####		MANAGER INSIGNIA		#####
#########################################
class InsigniaManager(models.Manager):
	def insigniasRestantes(self):
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute(""" SELECT * FROM HdaCautivo_BD.Insignia i WHERE i.cantidad>(SELECT count(*) FROM HdaCautivo_BD.hermanoLLevaInsignia ll WHERE i.id=ll.id_insignia AND YEAR(ll.fecha)=DATE_FORMAT(CURDATE(),'%Y'))ORDER BY i.nombre""")
		lista = []
		for row in cursor.fetchall():

			indice = int(row[1])
			subTramo = SubTramo.objects.get(id=indice)
			i = self.model (id=row[0],tramoAlQuePertenece=subTramo,nombre=row[2],cantidad=int(row[3]),precio=row[4],orden=int(row[5]))
			lista.append(i)
		return lista


class Insignia(models.Model):

	tramoAlQuePertenece = models.ForeignKey(SubTramo, related_name="Tramo al que pertenece la insignia", db_column="id_Tramo")
	nombre = models.CharField (max_length=40)
	cantidad = models.IntegerField()
	precio = models.FloatField()
	orden = models.IntegerField()
	objects = InsigniaManager()

	class Meta:
		db_table = "insignia"
		verbose_name = "Insignia"
		ordering = ['nombre']
		

	def __unicode__(self):
	    	return self.nombre



class Elemento(models.Model):
	pasoAlQuePertenece = models.ForeignKey(Paso, related_name="Paso al que pertenece el elemento", db_column="id_Paso")
	nombre = models.CharField(max_length=40)
	precio = models.FloatField()
	tipo = models.CharField(max_length=45)

	class Meta:
		db_table = "elemento"
		verbose_name = "Elemento"
		ordering = ['nombre']

	def __unicode__(self):
		return u'%s, del tipo %s'%(self.nombre,self.tipo)

class Cuadrilla(models.Model):
	pasoAlQuePertenece = models.ForeignKey(Paso, related_name="Paso al que pertenece el mienbro de la cuadrilla", db_column="id_Paso", verbose_name="Elige: ")
	nombre = models.CharField(max_length=40)
	precio = models.FloatField()

	class Meta:
		db_table = "cuadrilla"
		verbose_name = "Cuadrilla"
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre


#################################################################################################################
#####		HERMANOS COSTALEROS Y NAZARENOS QUE REALIZAN ESTACIÓN DE PENITENCIA (PAPELETAS DE SITIO)		#####
#################################################################################################################

					#########################################################################
					#####		ELEMENTOS RELACIONADOS CON EL TIPO TRAMO/INSIGNIA 		#####
					#########################################################################
class HermanoLLevaInsignia(models.Model):
	hermano = models.ForeignKey(HermanoDeAlta, related_name="Hermano que lleva la insignia", db_column="id_Hermano")
	insignia = models.ForeignKey(Insignia, related_name="Insignia que porta el hermano", db_column="id_Insignia")
	fecha = models.DateField(auto_now_add=True, verbose_name="año")

	class Meta:
		db_table = "hermanoLLevaInsignia"
		verbose_name = "Hermano que porta una insignia"
		verbose_name_plural = "Hermanos que portan insignias"

	def __unicode__(self):
	    return u'%s, %s --> %s /(%s)'%(self.hermano.apellidos,self.hermano.nombre,self.insignia.nombre,self.fecha)



					#################################################################
					#####		ELEMENTOS RELACIONADOS CON EL TIPO PASO 		#####
					#################################################################

class HermanoLLevaElemento(models.Model):
	hermano = models.ForeignKey(HermanoDeAlta, related_name="Hermano que lleva el elemento", db_column="id_Hermano")
	elemento = models.ForeignKey(Elemento, related_name="Elemento que lleva el hermano", db_column="id_Elemento")
	fecha = models.DateField(auto_now_add=True, verbose_name="año")
	idTramo = models.IntegerField(verbose_name="Tramo en el que procesiona", null=True, blank=True)
	numPareja = models.IntegerField(verbose_name="Fila dentro del tramo en la que procesiona", null=True, blank=True)

	class Meta:
		db_table = "hermanoLLevaElemento"
		verbose_name = "Hermano que lleva el elemento"
		verbose_name_plural = "Hermanos que llevan elementos"

	def __unicode__(self):
		return u'%s, %s --> %s [Tramo: %s] /(%s)'%(self.hermano.apellidos,self.hermano.nombre,self.elemento.nombre,self.idTramo,self.fecha)



class HermanoCuadrilla(models.Model):
	hermano = models.ForeignKey(HermanoDeAlta, related_name="Hermano que sale en una cuadrilla", db_column="id_Hermano")
	cuadrilla = models.ForeignKey(Cuadrilla, related_name="Paso en el que procesiona el hermano", db_column="id_Paso")
	fecha = models.DateField(auto_now_add=True, verbose_name="año")

	class Meta:
		db_table = "hermanoPerteneceACuadrilla"
		verbose_name = "Cuadrilla Costaleros/Capataces"
		verbose_name_plural = "Cuadrillas Costaleros/Capataces"

	def __unicode__(self):
		return u'%s, %s --> %s /(%s)'%(self.hermano.apellidos,self.hermano.nombre,self.cuadrilla.nombre,self.fecha)



#############################
#####		TUNICAS		#####
#############################
TUNICA_CHOICE =(
	('NAZARENO','NAZARENO'),
	('MONAGUILLO','MONAGUILLO'),
)
class Tunica(models.Model):
	hermano = models.ManyToManyField(HermanoDeAlta, through="tunicaAlquilerDelHermano")
	tipo = models.CharField(max_length = 20, choices = TUNICA_CHOICE)
	precio = models.FloatField(default=18.00)


	class Meta:
		db_table = "tunica"
		verbose_name = "Tunica"

	def __unicode__(self):
		return u'%s'%(self.tipo)


#####################################
#####		TUNICA/HERMANO		#####
#####################################
class tunicaAlquilerDelHermano(models.Model):
	hermano = models.ForeignKey(HermanoDeAlta, db_column="id_hermano")
	tunica = models.ForeignKey(Tunica, db_column="id_cuota")
	fecha = models.DateField(auto_now_add=True, verbose_name="Año del Alquiler de la tunica")
	devuelta = models.BooleanField(default = False, verbose_name="¿Ha sido devuelta?")


	class Meta:
		db_table = "tunicaAlquilerDelHermano"
		verbose_name = "Tunica alquilada por el hermano"
		verbose_name_plural = "Tunicas alquiladas por los hermanos"


