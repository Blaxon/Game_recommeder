"""
pc端程序的支持程序

作者：向航
2015-12-15
"""


import uuid
from urllib import request, error


def get_mac_address():
    """
    获得mac地址
    """
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac


def check_id(user_id):
    """
    检查id是否存在
    """
    try:
        check_url = 'http://127.0.0.1:8000/user/check/?id='
        content = request.urlopen(check_url+user_id).read()
        return content.decode()
    except error.URLError:
        print('Connection Error,Please check your connection.')
        return 'connection error'


def add_game_to_server(user_id, game_name):
    """
    向服务器账户添加游戏，返回another_name
    若报异常则返回Error
    """
    print('user: ', user_id, ' add game :', game_name)
    add_url = 'http://127.0.0.1:8000/user/addgame/?username=%s&game=%s'
    req_url = add_url % (user_id, request.quote(game_name))  # 使用quote对中文进行百分号编码
    content = request.urlopen(req_url).read().decode()
    if 'Game added' in content:
        another_name = content.split('\n')[1].strip().split('|')[-1]
        return another_name
    else:
        return "Error"


def del_game_from_server(user_id, game_name):
    """
    向服务器发送删除用户游戏请求
    :param user_id: 用户账号
    :param game_name: 游戏名称
    :return: 返回处理结果
    """
    del_url = 'http://127.0.0.1:8000/user/delgame/?username=%s&game=%s'
    req_url = del_url % (user_id, request.quote(game_name))
    content = request.urlopen(req_url).read().decode()
    if 'success' in content:
        return True
    else:
        return False


def update_time(user_id, another_name, play_time):
    """
    想服务器更新游戏时间
    """
    update_url = 'http://127.0.0.1:8000/user/updatetime/?username=%s&game=%s&time=%.4f'
    req_url = update_url % (user_id, request.quote(another_name), play_time)
    content = request.urlopen(req_url).read().decode()
    if 'complete' in content:
        return True
    else:
        raise Exception(content)


if __name__ == '__main__':
    def test1():
        """
        测试add_game_to_server
        """
        user_id = 'a45e60bad3c9'
        another_name = add_game_to_server('test', '88')
        print(another_name)

    test1()