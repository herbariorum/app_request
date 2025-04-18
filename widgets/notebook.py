import tkinter as tk
from tkinter import ttk


class NotebookRequest():
    def __init__(self, parent, main_app):
        
        self.parent = parent
        self.main_app = main_app

        self.init_components()

    
    def init_components(self):

        # Cria o notebook
        self.note = ttk.Notebook(self.parent)
        self.note.pack(fill='both', expand=True)
        self.note.bind('<Button-3>', self.close_tab)

        self.context_menu = tk.Menu(self.note, tearoff=0)
        self.context_menu.add_command(label="Fecha aba", command=lambda: self.close_current_tab(self.note.index(self.note.select())))

        

    def close_tab(self, event):       
        current_tab = self.note.index(self.note.select())        
        self.context_menu.post(event.x_root, event.y_root)
        self.context_menu.bind("<ButtonRelease-1>", lambda e: self.close_current_tab(current_tab))
        
    
    def close_current_tab(self, tab_index):
        """
        Fecha a aba especificada e remove-a do tab_mapping.
        """
        # Obtém o identificador da aba (tab_id)
        tab_id = self.note.tabs()[tab_index]

        # Remove a aba do Notebook
        self.note.forget(tab_index)

        for tree_item_id, mapped_tab_id in list(self.main_app.tab_mapping.items()):
            if mapped_tab_id == tab_id:
                del self.main_app.tab_mapping[tree_item_id]
                self.main_app.lista_de_request.get_lista_de_request().delete(tree_item_id)
                break

