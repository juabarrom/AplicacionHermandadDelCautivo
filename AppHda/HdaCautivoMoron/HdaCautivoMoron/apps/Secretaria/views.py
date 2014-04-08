# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from HdaCautivoMoron.apps.Secretaria.models import HermanoDeAlta
# Create your views here.

def indice_view(request):
	ctx ={}
	return render_to_response('SecretariaTemplates/indice.html',ctx, context_instance=RequestContext(request))


def datosHermano_view(request,idHermano):
	hermano = HermanoDeAlta.objects.filter(id=int(idHermano))
	ctx ={'hermano':hermano}
	return render_to_response('SecretariaTemplates/datosHermano.html',ctx, context_instance=RequestContext(request))
