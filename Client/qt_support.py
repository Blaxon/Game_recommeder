"""
pc端程序的支持程序

作者：向航
2015-12-15
"""


import uuid
from urllib import request


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
    check_url = 'http://127.0.0.1:8000/user/check/?id='
    content = request.urlopen(check_url+user_id).read()
    return content.decode()


def add_game_to_server(user_id, game_name):
    """
    向服务器账户添加游戏，返回another_name
    """
    print('user: ', user_id, ' add game :', game_name)
    add_url = 'http://127.0.0.1:8000/user/addgame/?username=%s&game=%s'
    req_url = add_url % (user_id, request.quote(game_name))
    content = request.urlopen(req_url).read().decode()
    print(req_url)
    if 'Game added' in content:
        another_name = content.split('\n')[1].strip().split('|')[-1]
        return another_name
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