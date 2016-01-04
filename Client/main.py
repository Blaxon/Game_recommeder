"""
这是pc端的实现
使用tkinter

主要实现以下功能：
1. 用户注册
2. 用户登录
3. 游戏添加
4. 游戏推荐
5. 游戏运行

作者：向航
"""
import os
import time
import traceback
import tkinter as tk
from tkinter.messagebox import showinfo, showerror


class Application(tk.Frame):
    """
    """

    game_dic = {}  # 存储游戏数据{'name':{'dir': str, 'hour': float}}

    def __init__(self):
        master = tk.Tk()
        master.title('Game recommend')
        master.geometry('280x400')
        master.resizable(width=False, height=True)
        tk.Frame.__init__(self, master)
        self.pack()

        self.top = tk.Label(self, text='你好，欢迎使用游戏推荐系统。请登录', fg='blue')
        self.top.bind('<Double-1>', self.user_login)
        self.top.pack(side='top')

        self.middle = tk.Frame(self, bg='LightSkyBlue')
        self.middle_sb = tk.Scrollbar(self.middle)
        self.middle_sb.pack(side='right', fill=tk.Y)
        self.middle_lb = tk.Listbox(self.middle, height=20, width=30, yscrollcommand=self.middle_sb.set)
        self.middle_lb.bind('<Double-1>', self.run_game)  # 这里将listbox中的双击动作作为打开游戏
        self.middle_sb.config(command=self.middle_lb.yview)
        self.middle_lb.pack(side='left', fill=tk.BOTH)
        self.middle.pack()

        self.bottom = tk.Frame(self)
        tk.Button(self.bottom, text='添加游戏', command=self.add_game).pack(side='left')
        tk.Button(self.bottom, text='游戏推荐').pack(side='right')
        self.bottom.pack(side='bottom')

        self.refresh()

    def user_register(self):
        pass

    def user_login(self, ev=None):
        print('login')
        pass

    def add_game(self):
        _ = AddGame(self)

    def run_game(self, ev=None):
        """
        启动游戏，并记录游戏时长
        游戏时长以小时单位计算
        """
        start_time = time.time()
        game_name = self.middle_lb.get(self.middle_lb.curselection())
        print('open', game_name)
        _dir = self.game_dic[game_name]['dir']
        output = os.system('%s' % _dir)  # 启动游戏
        game_time = (time.time() - start_time) / 3600
        print(game_time)
        self.game_dic[game_name]['hour'] += game_time

        try:
            _f = open('record', 'r+')
            _text = ''
            for line in _f.readlines():
                if game_name + '|' in line:
                    _text += '|'.join(line.split('|')[:2]) + '|%.4f\n' % game_time
                else:
                    _text += line
            _f.seek(0, 0)
            _f.write(_text)
            _f.close()
        except:
            traceback.print_exc()

    def recommend_game(self):
        pass

    def refresh(self):
        """
        读取record中的记录，更新game_dic并刷新主页面
        """
        try:
            self.game_dic = {}
            _f = open('record')
            self.middle_lb.delete(0, tk.END)
            for line in _f.readlines():
                print(line)
                _name, _dir, _hour = line.split('|')
                self.game_dic[_name] = {'dir': _dir,
                                        'hour': float(_hour)}
                self.middle_lb.insert(tk.END, _name)

            print(self.game_dic)
        except:
            traceback.print_exc()


class AddGame(Application):

    flag = 0  # 表示游戏是否添加成功的标签

    def __init__(self, father):
        self.father = father
        master = tk.Tk()
        master.title('添加游戏')
        master.geometry('240x80')
        master.resizable(width=False, height=True)
        tk.Frame.__init__(self, master)

        self.game_dir = tk.StringVar(master)
        self.game_name = tk.StringVar(master)
        self.dir = tk.Frame(self)
        tk.Label(self.dir, text='游戏路径 :').pack(side='left')
        tk.Entry(self.dir, textvariable=self.game_dir).pack(side='right')
        self.dir.pack()

        self.name = tk.Frame(self)
        tk.Label(self.name, text='游戏名称 :').pack(side='left')
        tk.Entry(self.name, textvariable=self.game_name).pack(side='right')
        self.name.pack()

        self.button = tk.Frame(self)
        add = tk.Button(self.button, text='添加', command=self.add)
        add.pack(side='left')
        tk.Button(self.button, text='退出', command=master.destroy).pack(side='right')
        self.button.pack()
        self.pack()

    def add(self):
        """
        为本地record文件添加相关信息，具体格式为：
        每一行为一个游戏信息；格式： 游戏名|游戏路径|游戏时间
        """
        _game_name = self.game_name.get()
        _game_dir = self.game_dir.get()

        if not os.path.isfile(_game_dir):
            showerror('错误', '游戏路径不正确，请重试！')
            return

        try:
            _f = open('record', 'r+')
            print(_f.read())
            _f.write('%s|%s|%d\n' % (_game_name, _game_dir, 0))
            _f.close()
            showinfo('提示', '游戏添加成功！')
            self.father.refresh()
        except:
            traceback.print_exc()


if __name__ == '__main__':
    app = Application()
    app.mainloop()