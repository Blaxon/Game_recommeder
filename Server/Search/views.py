from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(req):
    return HttpResponse("Hello World.You're at the Search index.")