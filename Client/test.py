import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.hi_there = tk.Button(self)
        self.hi_there['text'] = "Hello World\n(click me)"
        self.hi_there['command'] = self.say_hi
        self.hi_there.pack(side='top')

        self.QUIT = tk.Button(self, text='QUIT', fg='red', command=root.destroy)
        self.QUIT.pack(side='bottom')

        self.text = tk.Entry(self, text='hi')
        self.text.pack(side='left')

    def say_hi(self):
        print('hi there!')


root = tk.Tk()
app = Application(master=root)
app.mainloop()