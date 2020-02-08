#-*- coding: UTF-8 -*- 

from tkinter import *
import tkinter.font as tkFont
import random
import gc
import os, sys
import chardet
import copy
from threading import Thread
import time


def center_window(root, width, height):
    """
    :param root: tk
    :param width:
    :param height:
    :return:
    """
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


def clear():
    lb.delete(0, END)


def get_names():
    names = []
    name_path = os.path.join(BASE_DIR, 'name.txt')
    with open(name_path, 'rb') as f:
        data = f.read()
        cod = chardet.detect(data)['encoding']
        if 'gb' in str(cod):
            cod = 'gbk'
        for name in data.decode(cod).strip().split('\n'):
            if name.strip():
                names.append(name.strip())
        return names


class MyThread(Thread):
    def __init__(self):
        self.ifdo = False
        self.auto_choise = False
        self.is_auto = -1
        super().__init__()

    def run(self):
        while True:
            if self.is_auto is True:
                while self.ifdo:
                    index = random.randint(0, len(names) - 1)
                    echo["text"] = names[index]
                    root.update_idletasks()
                    time.sleep(1 / 23 - 0.003)
                self.is_auto = -1
            elif self.is_auto is False:
                if self.auto_choise:
                    self.auto()
                    self.is_auto = -1
            time.sleep(0.1)

    def stop(self):
        """
        stop process for 点击停止
        :return:
        """
        if self.is_auto:
            self.ifdo = False
            button2["text"] = '手动抽奖'
            _name = random.choice(names)
            echo["text"] = _name
            lb.insert(END, _name)
            root.update_idletasks()
            root.update()
            for x in locals().keys():
                del locals()[x]
            gc.collect()
            scrolly.update()

    def go(self):
        """
        Stop flag for manually stop
        :return:
        """
        if self.is_auto == -1:
            self.is_auto = True
            self.ifdo = True
            button2["text"] = '点击停止'

    def auto_start(self):
        """
        Change flad to auto
        :return:
        """
        if self.is_auto == -1:
            self.is_auto = False
            self.auto_choise = True
            button["text"] = '            '

    def auto(self):
        """
        自动开始时执行的操作
        :return:
        """
        copy_names = copy.deepcopy(names)
        ren = v
        for i in range(ren):
            for a in range(23):
                index = random.randint(0, len(names) - 1)
                echo["text"] = random.choice(names)
                root.update_idletasks()
                time.sleep(1 / 23 - 0.003)

            choise_name = copy_names.pop(random.choice(range(len(copy_names))))
            echo["text"] = choise_name

            lb.insert(END, choise_name)
            if i == ren - 1:
                button["text"] = '开始抽奖'
            for a in range(5):
                root.update()
                time.sleep(0.03)

        root.update_idletasks()

        for x in locals().keys():
            del locals()[x]
        gc.collect()

        scrolly.update()
        self.auto_choise = False


flag = False


def name2():
    global flag
    flag = not flag

    if flag:
        tr.go()
    else:
        tr.stop()


def name():
    tr.auto_start()


try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    names = get_names()

    root = Tk()

    root.title("抽奖冲鸭")

    center_window(root, 450, 150)

    echo = Label(root, text='???', font=('microsoft yahei', 15), width=20)  # 默认显示
    echo.grid(row=1, column=1, columnspan=2)

    scrolly = Scrollbar(root)
    scrolly.grid(row=1, column=4, rowspan=2, ipady=30)
    lb = Listbox(root, yscrollcommand=scrolly.set, exportselection=False, height=6)
    lb.grid(row=1, column=4, rowspan=2, columnspan=2, pady=0)
    scrolly['command'] = lb.yview

    button = Button(root, text='清除列表', command=clear)
    button.grid(row=3, column=4)

    v = 1

    button = Button(root, text='自动抽奖', command=name)
    button.grid(row=1, column=0, columnspan=1)
    flag = False

    button2 = Button(root, text='手动抽奖', command=name2)
    button2.grid(row=2, column=0, columnspan=1)

    tr = MyThread()
    tr.setDaemon(True)
    tr.start()

    root.mainloop()
except Exception as e:
    print('Error:', e)
    time.sleep(60)
