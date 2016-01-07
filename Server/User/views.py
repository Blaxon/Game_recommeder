from django.shortcuts import render
import traceback

# Create your views here.
import json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.template import loader, Context
from django.core.paginator import Paginator

from .models import User
from Search.models import GameInfo

USER_INFO = {}


def index(req):
    return HttpResponse("You're at User app.")


def check(req):
    """
    检查账户是否存在，如果不存在则新建
    """
    _id = req.GET['id']
    result = User.objects.get_or_create(username=_id)
    if result[1]:  # True 为新建账户
        return HttpResponse('new')
    else:
        return HttpResponse('exists')


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

        # 查找出该游戏的准确名称
        s = SearchQuerySet()
        _game_name = s.auto_query(_game_name)[0].name

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
            return HttpResponse('Game added\n%s' % _user.games)
        else:
            _user.games += '|' + _game_name
            _user.times += '|0'
            _user.save()
            return HttpResponse('Game added\n%s' % _user.games)

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
        times[_index] = _time
        _user.times = '|'.join(times)
        _user.save()
        return HttpResponse('update complete!')
    except Exception as e:
        traceback.print_exc()
        return HttpResponse('error occur')


def game_recommend(req):
    """
    加入了分页技术，添加了一个全局变量用以存储当前活跃用户的用户推荐表，以此来加快推荐列表读取速度。
    ---15.12.24更新---
    向用户推荐游戏；通过获取用户的游戏信息，我们查找其游戏的类型，并使用whoosh进行搜索其最匹配的游戏；
    按照得分高低，发行时间进行排序推荐。
    这里的输入为用户名称，我们自动的从后台调出用户数据。
    返回值为 列表
    """
    import time
    start_time = time.time()
    _user = req.GET['username']
    if _user in USER_INFO:
        print('user rec cache already exists.')
        _page = req.GET['page']
        p = USER_INFO[_user]
        p = p.page(_page)
    else:
        print('build new user rec cache...')
        _user_object = User.objects.get(username=_user)  # 用get替换了之前的filter，速度提高不少
        games = _user_object.games.split('|')
        dic_games = []
        s = SearchQuerySet()
        # 找到用户所玩的游戏
        for _game in games:
            item = GameInfo.objects.filter(name=_game)[0]
            if item not in dic_games:
                dic_games.append(item)
        # 找到对应类型游戏，每个类型取50个
        _map = {}
        for item in dic_games:
            if item.tag is None:
                continue
            tags = item.tag.strip().split(' ')
            for _tag in tags:
                corr_games = s.auto_query(_tag)[:20]
                for _ in corr_games:
                    if _.name not in _map:
                        _map[_.name] = 0
                    else:
                        _map[_.name] += 1

        sorted_games = sorted(_map.items(), key=lambda x: x[1], reverse=True)

        result = []
        for _game in sorted_games:
            result.append(GameInfo.objects.get(name=_game[0]))

        pagi = Paginator(result, 10)
        USER_INFO[_user_object.username] = pagi
        p = pagi.page(1)

    time_consume = (time.time() - start_time) * 1000
    print('%.5f seconds take.' % time_consume)

    # print(len(result))
    game_context = Context({'page': p,
                            'time': '%.5f' % time_consume,
                            'user': _user})
    temp = loader.get_template('Game_List.html')

    return HttpResponse(temp.render(game_context))
