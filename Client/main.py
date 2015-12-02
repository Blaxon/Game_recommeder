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
import tkinter as tk


class Application(tk.Frame):
    """
    """
    def __init__(self):
        master = tk.Tk()
        master.title('Game recommend')
        master.geometry('280x400')
        master.resizable(width=False, height=True)
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.top = tk.Label(self, text='你好，欢迎使用游戏推荐系统')
        self.top.pack(side='top')

        self.middle = tk.Text(self, width=35, height=21)
        self.middle.pack()

        self.bottom = tk.Frame()
        tk.Button(self.bottom, text='添加游戏').pack(side='left')
        tk.Button(self.bottom, text='游戏推荐').pack(side='right')
        self.bottom.pack(side='bottom')
        pass

    def user_register(self):
        pass

    def user_login(self):
        pass

    def add_game(self):
        pass

    def run_game(self):
        pass

    def recommend_game(self):
        pass


if __name__ == '__main__':
    app = Application()
    app.mainloop()