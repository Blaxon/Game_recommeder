from django.shortcuts import render
from django.template import Context, loader

# Create your views here.
from django.http import HttpResponse
from .models import GameInfo
from json import dumps


def index(req):
    return HttpResponse("Hello World.You're at the Search index.")


def form(req):  # 表页面函数
    return render(req, 'form.html')


def example_input(req):  # 处理表函数的应用
    a = req.GET['a']
    b = req.GET['b']
    return HttpResponse(int(a)+int(b))


def post_game(req):
    """
    生成单个游戏界面
    """
    _game_name = req.GET['name']
    game = GameInfo.objects.get(name=_game_name)
    c = Context({'game_name': game.name,
                 'game_info': game.introduction})
    t = loader.get_template('Single_Game.html')
    return HttpResponse(t.render(c))
