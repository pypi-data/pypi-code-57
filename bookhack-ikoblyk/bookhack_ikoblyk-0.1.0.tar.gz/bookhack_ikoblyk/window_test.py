#!/usr/bin/env python3

from tkinter import filedialog
from tkinter import *
import tkinter as tk
import os, re
from tkinter import messagebox
from bookhack_ikoblyk.test import Work


class Window:
    def __init__(self):
        self.reg = re.compile(r"^https://elib.nlu.org.ua/view.html\?&id=\d+")
        self.reg2 = re.compile(r"^[']?(?:/[^/]+)*[']?$")
        self.all_valid = False
        self.root = Tk(className='myTkApp')
        self.root.title("Скачати книжку")
        self.path_text = ''
        self.url_text = ''
        self.text_path = ''
        self.finished = False
        self.url = tk.Label(self.root, text="Виберіть ссилку").grid(row=0)
        self.path = tk.Label(self.root, text="Вибраний шлях: ").grid(row=1)
        self.e1 = tk.Entry(self.root)
        self.e2 = tk.Entry(self.root)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.submitButton = Button(self.root, command=self.buttonClick, text="Виберіть шлях")
        self.submitButton_final = Button(self.root, command=self.regex_check, text="Підтвердити усе і завершити")
        self.submitButton.grid(row=3, column=1)
        self.submitButton_final.grid(row=4, column=3)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def regex_check(self):
        if self.e1.index("end") != 0:
            self.url_text = self.e1.get()
            print(self.url_text)

        if self.e2.index("end") != 0:
            self.text_path = self.e2.get()
            print(self.text_path)

        if self.reg.fullmatch(self.url_text) is not None and self.reg2.fullmatch(self.path_text) is not None:
            self.all_valid = True
            w = Work(self.path_text, self.url_text)
            messagebox.showinfo("Почати", " Натисни ок щоб почати скачування(Закривати програму не рокомендуємо)")
            self.finished = w.run()
            messagebox.showinfo("Файли скачені", "Скрипт зконвертує їх сам")



        else:
            messagebox.showerror(f"{self.path_text}Помилка", "Перевір дані")


    def create_window(self):
        window = tk.Toplevel(self.root)

    def run(self):
        self.root.mainloop()

    def path_checker(self):
        if self.e2.index("end") != 0:
            self.text_path = self.e2.get()
            print(self.text_path)

    def on_closing(self):
         if self.all_valid is False or self.finished is True:
            self.root.destroy()

         elif messagebox.askokcancel("Процес іде...", "Може статися помилка. Точно?") and self.all_valid is True and self.finished is False:
            self.root.destroy()

    def buttonClick(self):
        folder_selected = filedialog.askdirectory(initialdir = '/home/ivan/Documents')
        self.e2.delete(first=0, last=100)
        print(folder_selected)
        if type(folder_selected) != tuple:
            print(os.path.split(folder_selected))
            path = "/".join(os.path.split(folder_selected))
            self.e2.insert(0, path)
            self.path_text = path

    def url_checker(self):
        if self.e1.index("end") != 0:
            self.url_text = self.e1.get()
            print(self.url_text)

