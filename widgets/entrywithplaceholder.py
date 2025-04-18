# import tkinter as ttk
from tkinter import ttk

class EntryWithPlaceholder(ttk.Entry):
    def __init__(self, master=None, placeholder="", placeholder_color="gray",  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.default_fg_color = self["foreground"]
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
       
        self._add_placeholder()

    def _clear_placeholder(self, event=None):
        # Remove o placeholder se o texto atual for igual ao placeholder
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self["foreground"] = self.default_fg_color

    def _add_placeholder(self, event=None):
        # Adiciona o placeholder se o campo estiver vazio
        if not self.get():
            self.insert(0, self.placeholder)
            self["foreground"] = self.placeholder_color