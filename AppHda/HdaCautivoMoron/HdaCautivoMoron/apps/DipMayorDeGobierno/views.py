# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from HdaCautivoMoron.apps.Secretaria.models import HermanoDeAlta as ha
from HdaCautivoMoron.apps.DipMayorDeGobierno.models import Paso, HermanoLLevaInsignia, Insignia, HermanoLLevaElemento, Elemento
from HdaCautivoMoron.apps.DipMayorDeGobierno.forms import formBuscadorHermano, formPapeletaInsignia, formLuces, formPapeletaCuadrilla, formInsignia
from django.core.paginator import Paginator,EmptyPage,InvalidPage
import datetime
#PISA
import ho.pisa as pisa
import cStringIO as StringIO
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
import os
import cgi



# Create your views here.
def indicedipMayorDeGobierno_view(request):

	if request.method == 'POST':
		print "POST"
		buscadorHermano = formBuscadorHermano(request.POST)
		if buscadorHermano.is_valid():

			stringConsultaHermano = buscadorHermano.cleaned_data['hermano']
			listaConsultaHermano = stringConsultaHermano.split(" ")

			solAux =[]
			for cadena in listaConsultaHermano:
				aux = ha.objects.filter(activo=True).filter(Q(apellidos__icontains=cadena) | Q(nombre__icontains=cadena))
				queryConsulta = set(aux)
				solAux.append(queryConsulta)

			sol = set(solAux[0])
			for query in solAux:
				sol = sol & query

			
			#CREAR SESION CON LOS ID DE LA SOLUCION
			listaSession = []
			for idH in sol:
				listaSession.append(int(idH.id))

			request.session["coincidenciasSesion"] = list(listaSession)


			#REDIRIGIR
			return redirect('vista_mostrarCoincidencia',pagina = int(1))
			

		else:
			buscadorHermano = formBuscadorHermano(request.POST)
			ctx = {'form':buscadorHermano}
			return render_to_response('DipMayorDeGobiernoTemplates/indice.html', ctx, context_instance=RequestContext(request))
	else:
		print "GET"
		buscadorHermano = formBuscadorHermano()
		ctx = {'form':buscadorHermano}
		return render_to_response('DipMayorDeGobiernoTemplates/indice.html', ctx, context_instance=RequestContext(request))




def historialDeLaCofradia_view(request):

	anyoActual = datetime.datetime.now().year

	#ELEMENTOS
	numLuces = HermanoLLevaElemento.objects.filter(fecha__year=anyoActual).count()
	numLucesCristo = HermanoLLevaElemento.objects.filter(elemento__nombre="CIRIO PASO CRISTO").filter(fecha__year=anyoActual).count()
	numLucesVirgen = HermanoLLevaElemento.objects.filter(elemento__nombre="CIRIO PASO VIRGEN").filter(fecha__year=anyoActual).count()

	#INSIGNIAS
	insignias = Insignia.objects.all()
	hermanoInsginia = HermanoLLevaInsignia.objects.filter(fecha__year=anyoActual)

	#CUADRILLA

	#CONTEXTO
	ctx = {'fecha': anyoActual,'numLuces':numLuces, 'numLucesCristo':numLucesCristo, 'numLucesVirgen':numLucesVirgen, 'insignias':insignias, 'hermanoInsginia':hermanoInsginia}
	
	return render_to_response('DipMayorDeGobiernoTemplates/historialCofradia.html', ctx, context_instance=RequestContext(request))



def mostrarCoincidencia_view(request,pagina):
	lista = []
	sol = []
	if "coincidenciasSesion" in request.session:
		lista = request.session["coincidenciasSesion"]
		for l in lista:
			aux = ha.objects.filter(id=int(l))
			sol.extend(aux)

	print sol

	print "NUMERO DE COINCIDENCIAS :::: %s"%(len(sol))	
	#PAGINACION DE HERMANOS
	paginator = Paginator(sol,5)

	try:
		page = int(pagina)

	except:
		page = 1
	
	try:
		listaCoincidencia = paginator.page(page)
	except (EmptyPage,InvalidPage):
		listaCoincidencia = paginator.page(paginator.num_pages)

	ctx = {'listaCoincidencia':listaCoincidencia}

	return render_to_response('DipMayorDeGobiernoTemplates/mostrarCoincidencia.html', ctx, context_instance=RequestContext(request))



def papeletaDeSitio_view(request,idHermano):

	insignia = "INSIGNIA"
	luces = "LUCES"
	cuadrilla = "CUADRILLA"

	if request.method == 'POST':
		stringTipoPregunta = request.POST['tipoPregunta']
		
		if stringTipoPregunta == insignia:
			print "ENTRA"
			return redirect('vista_papeletaDeSitioInsignia',idHermano = int(idHermano))
		if stringTipoPregunta == luces:
			print "ENTRA"
			return redirect('vista_papeletaDeSitioLuces',idHermano = int(idHermano))
		if stringTipoPregunta == cuadrilla:
			print "ENTRA"
			return redirect('vista_papeletaDeSitioCuadrilla',idHermano = int(idHermano))

	else:
		hermano = ha.objects.get(id=int(idHermano))
		papeletaInsignia =formPapeletaInsignia()
		ctx = {'hermano':hermano, "formPapeletaInsignia":papeletaInsignia}
		
		return render_to_response('DipMayorDeGobiernoTemplates/papeletasDeSitio.html',ctx, context_instance=RequestContext(request))





def papeletaDeSitioInsignia_view(request,idHermano):
	print "INSIGNIA"
	print idHermano

	if request.method == 'POST':
		stringInsignia = request.POST['insignia']

		hermano = ha.objects.get(id=int(idHermano))
		insignia = Insignia.objects.get(id=int(stringInsignia))
		fecha = datetime.datetime.now()

		hlli = HermanoLLevaInsignia(hermano=hermano,insignia=insignia,fecha=fecha)
		hlli.save()
		
		html = render_to_string('DipMayorDeGobiernoTemplates/papeletaSitioPDF.html', {'pagesize':'A4','nombre':hermano.nombre, 'apellidos':hermano.apellidos,'numHermano':hermano.numHermano, 'dni':hermano.dni, 'lugarEnLaCofradia':insignia.nombre, 'precio':insignia.precio}, context_instance=RequestContext(request))
		return generar_pdf(html)
	else:
		insignia = formInsignia()
		ctx={'form':insignia}
		return render_to_response('DipMayorDeGobiernoTemplates/insignia.html', ctx, context_instance=RequestContext(request))


def papeletaDeSitioLuces_view(request,idHermano):
	print "LUCES"
	print idHermano

	if request.method == 'POST':
		luces = formLuces(request.POST)
		if luces.is_valid():
			objLuces = luces.save(commit = False)
			objLuces.hermano = ha.objects.get(id= int(idHermano))
			print "Hermano"
			print objLuces.hermano.nombre
			objLuces.save()
		
		html = render_to_string('DipMayorDeGobiernoTemplates/papeletaSitioPDF.html', {'pagesize':'A4','nombre':objLuces.hermano.nombre, 'apellidos':objLuces.hermano.apellidos,'numHermano':objLuces.hermano.numHermano, 'dni':objLuces.hermano.dni, 'lugarEnLaCofradia':objLuces.elemento.nombre, 'precio':objLuces.elemento.precio}, context_instance=RequestContext(request))
		return generar_pdf(html)
	else:
		luces = formLuces()
		ctx = {'form':luces}
		return render_to_response('DipMayorDeGobiernoTemplates/luces.html', ctx, context_instance=RequestContext(request))





def papeletaDeSitioCuadrilla_view(request,idHermano):
	print "CUADRILLA"
	print idHermano

	if request.method == 'POST':
		papeletaCuadrilla = formPapeletaCuadrilla(request.POST)
		
		objPapeletaCuadrilla = papeletaCuadrilla.save(commit=False)
		objPapeletaCuadrilla.hermano = ha.objects.get(id=int(idHermano))
		objPapeletaCuadrilla.save()

		html = render_to_string('DipMayorDeGobiernoTemplates/papeletaSitioPDF.html', {'pagesize':'A4','nombre':objPapeletaCuadrilla.hermano.nombre, 'apellidos':objPapeletaCuadrilla.hermano.apellidos,'numHermano':objPapeletaCuadrilla.hermano.numHermano, 'dni':objPapeletaCuadrilla.hermano.dni, 'lugarEnLaCofradia':objPapeletaCuadrilla.cuadrilla.nombre, 'precio':objPapeletaCuadrilla.cuadrilla.precio}, context_instance=RequestContext(request))
		return generar_pdf(html)

	else:
		hermanoCostalero = formPapeletaCuadrilla()
		ctx = {'form':hermanoCostalero}
		return render_to_response('DipMayorDeGobiernoTemplates/cuadrilla.html', ctx, context_instance=RequestContext(request))




##################################
######		GENERAR PDF		######
##################################

def generar_pdf(html):
	result = StringIO.StringIO()
	print "generar_pdf"
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), dest = result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return HttpResponse ('Error al generar el PDF: %s' % cgi.escape(html))








