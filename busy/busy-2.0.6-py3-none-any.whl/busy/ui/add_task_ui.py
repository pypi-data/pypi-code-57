import tkinter as tk


class AddTaskUi(tk.Frame):  # pragma: no cover

    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Tk()
        self.root.state('zoomed')
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)
        frame = tk.LabelFrame(main, text="Task")
        self.entry = tk.Entry(frame, width=100)
        self.entry.bind('<Return>', self.enter)
        self.entry.pack()
        self.entry.focus()
        frame.pack(padx=20, pady=20)
        self.root.mainloop()

    def enter(self, event):
        value = self.entry.get()
        self.root.destroy()
        self.callback(value)
