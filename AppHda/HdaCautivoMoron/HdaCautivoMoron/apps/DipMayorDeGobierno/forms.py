# -*- coding: utf-8 -*-
from django import forms
from django.db import models, connection
from HdaCautivoMoron.apps.Secretaria.models import HermanoDeAlta
from HdaCautivoMoron.apps.DipMayorDeGobierno.models import Elemento, HermanoLLevaElemento, HermanoLLevaInsignia, Insignia, HermanoCuadrilla

class formBuscadorHermano(forms.Form):
	hermano = forms.CharField(label="Nombre/Apellidos del Hermano", max_length=30, required=True)



class formPapeletaInsignia(forms.Form):
	Asuntos = (
		('INSIGNIA','INSIGNIA'),
		('LUCES','LUCES'),
		('CUADRILLA','CUADRILLA'),
	)
	
	tipoPregunta = forms.ChoiceField(choices=Asuntos, label="ELIJA EL SITIO QUE VA A OCUPAR EN LA COFRADIA")


class formLuces(forms.ModelForm):
	
	class Meta:
		model = HermanoLLevaElemento
		exclude = ['hermano','idTramo','numPareja',]



class formPapeletaCuadrilla(forms.ModelForm):

	class Meta:
		model = HermanoCuadrilla
		exclude = ['hermano',]

class formInsignia(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(formInsignia, self).__init__(*args, **kwargs)
		
		#queryset= Insignia.objects.all()
		self.fields['insignia'].choices = [(insignia.id, insignia.nombre) for insignia in Insignia.objects.insigniasRestantes()]


	class Meta:
		model = HermanoLLevaInsignia
		exclude = ['hermano',]

