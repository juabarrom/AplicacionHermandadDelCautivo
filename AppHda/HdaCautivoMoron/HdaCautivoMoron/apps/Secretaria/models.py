# -*- coding: utf-8 -*- 
from django.db import models

ESTADOCIVIL_CHOICE = (
	('SOLTERO','SOLTERO/A'),
	('CASADO','CASADO/A'),
	('VIUDO','VIUDO/A'),
)

FORMACOBRO_CHOICE = (
	('COBRADOR','COBRADOR'),
	('BANCO','BANCO'),
)

SEXO_CHOICE = (
	('HOMBRE','HOMBRE'),
	('MUJER','MUJER'),
)
class HermanoDeAlta(models.Model):

	#DATOS PERSONALES
	numHermano = models.IntegerField()
	nombre = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)

	dni = models.CharField(max_length= 11, blank=True)
	#fechaAlta = models.DateField(auto_now_add=True)
	fechaAlta = models.DateField(blank=True, null=True)
	fechaNacimiento = models.DateField(blank=True, null=True)
	domicilio = models.CharField(max_length=200)
	localidad = models.CharField(max_length=100)
	provincia = models.CharField(max_length=100)
	codPostal = models.PositiveIntegerField()
	telefono = models.PositiveIntegerField(blank=True, null=True)
	movil = models.PositiveIntegerField(blank=True, null=True)
	email = models.EmailField(blank=True)
	sexo = models.CharField(max_length=10, choices=SEXO_CHOICE)
	estadoCivil = models.CharField(max_length=20,choices=ESTADOCIVIL_CHOICE) 
	activo = models.BooleanField(default=True, verbose_name="¿Activo?")

	#DATOS DE COBRO
	formaDePago = models.CharField(max_length=20, choices=FORMACOBRO_CHOICE)

	#COBRADOR
	domicilioCobro = models.CharField(max_length=200, blank=True)
	localidadCobro = models.CharField(max_length=100, blank=True)
	provinciaCobro = models.CharField(max_length=100, blank=True)
	codPostalCobro = models.PositiveIntegerField(blank=True, null=True)	

	#BANCARIOS
	nombreTitular = models.TextField(blank=True)
	apellidosTitular = models.TextField(blank=True)
	iban = models.CharField(max_length=4, blank=True, null=True)
	entidad = models.CharField(max_length=10, blank=True, null=True)
	oficina = models.CharField(max_length=10, blank=True, null=True)
	digitControl = models.CharField(max_length=2, blank=True, null=True)
	numCuenta = models.CharField(max_length=10, blank=True, null=True)
	

	class Meta:
		db_table = "hermanoDeAlta"
		verbose_name = "Hermano"
		verbose_name_plural = "Hermanos"
		ordering = ['numHermano']


	def __unicode__(self):
	    	return u'%s, %s'%(self.apellidos,self.nombre)

MOTIVO_CHOICES = (
	('DEFUNCION','DEFUNCION'),
	('VOLUNTAD','VOLUNTAD PROPIA'),
	('IMPAGOS','IMPAGOS DE RECIBOS'),
)
class HermanoDeBaja(models.Model):

	hermano = models.ForeignKey(HermanoDeAlta, related_name="Relacion de HermanoDeBaja con HermanoDeAlta", db_column="id_hermano")
	fechaBaja = models.DateField()
	motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)

	class Meta:
		db_table = "hermanoDeBaja"
		verbose_name = "Hermano de baja"
		verbose_name_plural = "Hermanos de baja"
		ordering = ['fechaBaja']


	def __unicode__(self):
	    	return u'%s, %s'%(self.hermano.apellidos,self.hermano.nombre)


TIPOENTIDAD_CHOICE = (
	('PROVEEDORES','PROVEEDORES'),
	('BANCO','ENTIDADES BANCARIAS'),
	('HERMANDADES','HERMANDADES'),
	('IGLESIA','PARROQUIA Y ENTIDADES ECLESIÁSSTICAS'),
	('OTRO','OTRO'),
)	


#################################
#####		ENTIDADES		#####
#################################

class Entidad(models.Model):
	tipo = models.CharField (max_length=10, choices=TIPOENTIDAD_CHOICE)
	nombre = models.TextField(blank=True)
	apodo = models.CharField(max_length=100, blank=True)
	domicilio = models.CharField(max_length=200, blank=True)
	localidad = models.CharField(max_length=100, blank=True)
	provincia = models.CharField(max_length=100, blank=True)
	codPostal = models.PositiveIntegerField(blank=True, null=True)
	telefono = models.PositiveIntegerField(blank=True, null=True)
	email = models.EmailField(blank=True)
	twitter = models.CharField(max_length=100, blank=True)
	facebook = models.CharField(max_length=100, blank=True)
	descripcion = models.TextField(blank=True)
	estado = models.BooleanField(default=True, verbose_name='¿Estado en la Entidad?')

	class Meta:
		db_table = "entidad"
		verbose_name = "Entidad"
		verbose_name_plural = "Entidades"


	def __unicode__(self):
	    	return self.apodo

#############################
#####		CUOTAS		#####
#############################

CATEGORIA_CHOICE =(
	('COBRADOR','PAGO ANUAL'),
)
class Cuota(models.Model):
	hermano = models.ManyToManyField(HermanoDeAlta, through="pagoCuotaDelHermano")
	precio = models.FloatField()
	categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICE)

	class Meta:
		db_table = "cuota"
		verbose_name = "Cuota"

	def __unicode__(self):
		return u'%s --> %s€'%(self.categoria,self.precio)

#####################################
#####		CUOTAS/HERMANO		#####
#####################################
class pagoCuotaDelHermano(models.Model):
	hermano = models.ForeignKey(HermanoDeAlta, db_column="id_hermano")
	cuota = models.ForeignKey(Cuota, db_column="id_cuota")
	fecha = models.DateField(verbose_name="Año de la Cuota")

	class Meta:
		db_table = "pagoCuotaDelHermano"
		verbose_name = "Pago de la Cuota por parte del hermano"
		verbose_name_plural = "Pagos de las Cuotas por parte de los hermanos"
