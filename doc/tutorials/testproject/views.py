from django.http import HttpResponse
from django.shortcuts import render_to_response

from testproject.models import *

def index(request):
	m = Test.objects.all()
	return render_to_response("index.html", { "tplvar1": m})

def testindex(request, id):
	getvar = request.GET.get("hi", "")
	m = Test()
	m.name = getvar
	m.save()
	return HttpResponse("<html><body><h1> " + id + getvar + " </hi></body></html>")
