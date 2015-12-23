"""
使用pyqt5来制作界面。

作者：向航
2015-12-15
"""
import os
import time
import traceback
import psutil

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *

from qt_addGame import *
from qt_support import *


class GameRecommend(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.games = {}  # 存储游戏数据的列表，从record文件中读取。里面有游戏名、游戏路径和游戏时间信息
        self.id = get_mac_address()
        local_game = QLabel('本地游戏')
        game_recommend = QLabel('游戏推荐')
        self.local_game = QListWidget()
        self.recommend_page = QWebView()  # 现在不知道怎么把这个东西加进去,先用tmp填补空缺
        add_btn = QPushButton('添加游戏')
        refresh_btn = QPushButton('刷新')

        add_btn.clicked.connect(self.add_game)
        refresh_btn.clicked.connect(self.refresh)
        self.local_game.doubleClicked.connect(self.run_game)

        grid_layout = QGridLayout()
        grid_layout.addWidget(local_game, 1, 0, 1, 1)
        grid_layout.addWidget(add_btn, 1, 1, 1, 1)
        grid_layout.addWidget(game_recommend, 1, 2, 1, 1)
        grid_layout.addWidget(refresh_btn, 1, 48, 1, 1)
        grid_layout.addWidget(self.local_game, 2, 0, 1, 2)
        tmp = QTextEdit()
        grid_layout.addWidget(self.recommend_page, 2, 2, 1, 48)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(20, 5, 20, 5)
        dlgLayout.addLayout(grid_layout)

        self.setLayout(dlgLayout)
        self.setWindowTitle("游戏推荐系统")
        self.resize(680, 480)

        self.load()
        self.refresh()
        self.check()

    def add_game(self):
        """
        跳转到添加游戏界面，并添加游戏
        """
        self.x = AddGame(self)
        self.x.show()

    def del_game(self):
        pass

    def refresh(self):
        """
        重载界面，目的包括：更新推荐列表、更新游戏列表
        """
        print('refresh')
        # 更新游戏列表
        self.local_game.clear()
        for item in sorted(self.games.items()):
            self.local_game.insertItem(0, item[0])

        # 更新推荐列表
        url = 'http://127.0.0.1:8000/user/recommend/?username=%s&page=1' % self.id
        self.recommend_page.load(QUrl(url))
        self.show()

    def run_game(self):
        """
        运行游戏，并记录游戏时间,退出游戏后更新后台游戏时间
        """
        start_time = time.time()
        game_name = self.local_game.selectedItems()[0].text()
        _dir = self.games[game_name]['dir'].replace(' ', r'\ ')  # 这里是将路径中的空格转换为shell可读的'\ '方式
        print("run game...", _dir)
        os.system('open %s' % _dir)

        process_name = self.games[game_name]['dir'].split('/')[-1][:-4]  # 从路径中截取出进程的名称
        print('process name identified: ', process_name)

        # 找到进程pid
        for _proc in psutil.process_iter():
            try:
                if _proc.name() and process_name in _proc.name():
                    print('process pid identified :', _proc.pid)
                    process_pid = _proc.pid
            except psutil.NoSuchProcess:
                pass

        while psutil.pid_exists(process_pid):
            pass

        play_time = time.time() - start_time
        print('game closed. play time: %.4f' % play_time)
        self.games[game_name]['time'] += play_time
        update_time(self.id, self.games[game_name]['another_name'], self.games[game_name]['time'])
        print('time updated. now total time %.2f' % self.games[game_name]['time'])

    def load(self):
        """
        在程勋刚开始运行时，（前提：self.games为空）
        读取record文件，并以列表形式返回信息。
        """
        try:
            _f = open('qt_record')
            for line in _f.readlines():
                _name, _dir, _time, _another_name = line.split('|')
                self.games[_name] = {'dir': _dir,
                                     'time': float(_time),
                                     'another_name': _another_name.strip()}
            _f.close()
        except :
            traceback.print_exc()

    def closeEvent(self, QCloseEvent):
        """
        关闭之前，把数据写入qt_record文件中
        同时同步后台服务器
        """
        try:
            _f = open('qt_record', 'r+')
            for item in self.games.items():
                print('write---', item)
                line = item[0] + '|' + item[1]['dir'] + '|' + '%.4f' % item[1]['time'] + \
                       '|' + item[1]['another_name'] + '\n'
                _f.write(line)
            _f.close()
        except:
            traceback.print_exc()

        super(GameRecommend, self).closeEvent(QCloseEvent)

    def check(self):
        """
        登陆服务器，如果没有这台电脑，则创建账号
        """
        print('run check.')
        content = check_id(self.id)
        if content == 'new':  # 当前用户不存在
            print('new id, creating new account...')
            # 这是一个非常有趣的动作，实际上当发现这个新用户的时候，它是不可能就已经添加过游戏的，所以这只是调试所用
            for key in self.games:
                assert add_game_to_server(self.id, key)
                print('game %s added into server.' % key)
        elif content == 'exists':
            print('user already exists.')
            return
        else:
            print('error. incorrect message received.')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gr = GameRecommend()
    gr.show()
    sys.exit(app.exec())