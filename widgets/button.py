from tkinter import ttk

class BButton(ttk.Button):
    def __init__(self, master=None, text=None, command=None):
        super().__init__(master, text=text, command=command)
        
        self.configure(style="Primary.TButton", width=20)
        
        