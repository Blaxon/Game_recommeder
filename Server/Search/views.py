from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(req):
    return HttpResponse("Hello World.You're at the Search index.")


def form(req):  # 表页面函数
    return render(req, 'form.html')


def example_input(req):  # 处理表函数的应用
    a = req.GET['a']
    b = req.GET['b']
    return HttpResponse(int(a)+int(b))
