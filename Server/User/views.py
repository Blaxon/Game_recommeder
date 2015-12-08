from django.shortcuts import render
import traceback

# Create your views here.
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from .models import User
from Search.models import GameInfo


def index(req):
    return HttpResponse("You're at User app.")


def register(req):
    """
    建立新账户
    """
    _user_name = req.GET['username']
    User.objects.create(username=_user_name)
    return HttpResponse('register complete!\nHello %s!' % _user_name)


def add_game(req):
    """
    添加新游戏
    接收的信息有：username|game
    更新游戏列表，同时更新游戏时间列表
    """
    try:
        _user_name = req.GET['username']
        _game_name = req.GET['game']

        _user = User.objects.filter(username=_user_name)
        if len(_user) == 0:
            return HttpResponse('User does not exists! check again!')

        # 添加游戏
        _user = _user[0]
        if _user.games is not None and _game_name in _user.games:
            return HttpResponse('game already exists!')
        if _user.games is None:
            _user.games = _game_name
            _user.times = '0'
            _user.save()
            return HttpResponse('Game added!----%s' % _user.games)
        else:
            _user.games += '|' + _game_name
            _user.times += '|0'
            _user.save()
            return HttpResponse('Game added!----%s' % _user.games)

    except Exception as e:
        traceback.print_exc()
        return HttpResponse('error occur')


def update_time(req):
    """
    更新游戏时间，一次更新一个游戏
    接受的信息有：username|game|time
    """
    try:
        _user_name = req.GET['username']
        _game = req.GET['game']
        _time = req.GET['time']  # str

        _user = User.objects.filter(username=_user_name)[0]
        games = _user.games.split('|')
        if _game not in games:
            return HttpResponse("This game is not in user's game list.")
        _index = games.index(_game)
        times = _user.times.split('|')
        times[_index] = str(float(times[_index]) + float(_time))
        _user.times = '|'.join(times)
        _user.save()
        return HttpResponse('update complete!')
    except Exception as e:
        traceback.print_exc()
        return HttpResponse('error occur')


def game_recommend(req):
    """
    向用户推荐游戏；通过获取用户的游戏信息，我们查找其游戏的类型，并使用whoosh进行搜索其最匹配的游戏；
    按照得分高低，发行时间进行排序推荐。
    这里的输入为用户名称，我们自动的从后台调出用户数据。
    返回值为 列表
    """
    _user = req.GET['username']
    _user = User.objects.filter(username=_user)[0]
    games = _user.games.split('|')
    dic_games = []
    s = SearchQuerySet()
    # 找到用户所玩的游戏
    for _game in games:
        item = s.auto_query(_game)[0]
        if item not in dic_games:
            dic_games.append(item)
    # 找到对应类型游戏，每个类型取50个
    _map = {}
    for item in dic_games:
        if item.tag is None:
            continue
        tags = item.tag.strip().split(' ')
        for _tag in tags:
            corr_games = s.auto_query(_tag)[:50]
            for _ in corr_games:
                if _.name not in _map:
                    _map[_.name] = 0
                else:
                    _map[_.name] += 1

    sorted_games = sorted(_map.items(), key=lambda x: x[1], reverse=True)

    result = []
    for _game in sorted_games:
        result.extend(GameInfo.objects.filter(name=_game[0]))

    print(result)

    return HttpResponse(result)