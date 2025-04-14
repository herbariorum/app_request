from tkinter import ttk
import tkinter as tk
from pathlib import Path
from PIL import ImageTk, Image

from styles import ConfigStyles
from widgets.sidebar import Sidebar
from widgets.notebook import NotebookRequest

from util.save_data import save_config_data, load_treeview_data

# Localização das imagens
IMG_PATH = Path(__file__).parent / 'images'

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ConfigStyles()  # Certifique-se de chamar isso aqui
       
        self.lista_de_request = None
        self.frame_do_meio = None
        self.frame_da_direita = None
        self.tab_mapping = {}
       
        self.pointer_icon = ImageTk.PhotoImage(Image.open(IMG_PATH/'6637787_direction_menu_point_pointer_icon.png').resize((16, 16)))

        self.after(100, self.maximize)

        painelPrincipal = tk.PanedWindow(
            self, 
            orient='horizontal',
            background="#4e4e4e",
            borderwidth=2,
            relief='flat',
            sashwidth=5,
            sashrelief='flat',
            handlesize=10,
            handlepad=5
        )
        painelPrincipal.pack(expand=True, fill='both')

        painelPrincipal.grid_columnconfigure(0, weight=0) # coluna não expande
        painelPrincipal.grid_columnconfigure((1, 2), weight=1) # colunas podem expandir
        painelPrincipal.grid_rowconfigure(0, weight=1) # linha expande

        # Painel de Exibição dos Requests em um treeview
        self.frame_sidebar = ttk.Frame(painelPrincipal, border=1, borderwidth=2)

        # Cria a Sidebar
        self.lista_de_request = Sidebar(self.frame_sidebar, self)
        # self.lista_de_request._lista_de_request.bind("<Double-1>", self.update_notebook)
        
        # Painel de Edição/Configuração dos Requests
        self.frame_do_meio = ttk.Frame(painelPrincipal, width=740, border=1, borderwidth=2)
        
        self.config_notebook = NotebookRequest(self.frame_do_meio, self)

        # Painel de Resultados dos Requests
        self.frame_da_direita = ttk.Frame(painelPrincipal)
        
        # Exibe os frames
        self.frame_sidebar.grid(row=0, column=0, sticky='ns')
        self.frame_do_meio.grid(row=0, column=1, sticky='nsew')
        self.frame_da_direita.grid(row=0, column=2, sticky='nsew')

        # Adiciona todas as  frames mo PanelWindow
        painelPrincipal.add(self.frame_sidebar)
        painelPrincipal.add(self.frame_do_meio)
        painelPrincipal.add(self.frame_da_direita)

        self.load_data_config()
        
    

    def update_notebook(self, method='GET', text=None, tree_item_id=None):        
        """
        Atualiza ou cria uma aba no Notebook com base no tree_item_id.
        """ 
        if tree_item_id in self.tab_mapping:           
            # Aba já existe, atualiza o texto da aba se necessário
            tab_id = self.tab_mapping[tree_item_id]
            if tab_id in self.config_notebook.note.tabs():
                self.config_notebook.note.tab(tab_id, text=text)
            else:
                print(f"Tab ID {tab_id} não encontrado no Notebook.")
        else: 
            
             # Cria uma nova aba
            tab_frame = ttk.Frame(self.config_notebook.note)
            self.config_notebook.note.add(tab_frame, text=text)
            tab_id = str(tab_frame)  # Usa o identificador do tab_frame como tab_id
            # Mapeia o tree_item_id para o novo tab_id
            if tree_item_id:
                self.tab_mapping[tree_item_id] = tab_id  # Corrigido para usar tree_item_id como chave
      

    def save_data_config(self, method='GET'):
        tree_data = []
        for item_id in self.lista_de_request._lista_de_request.get_children():
            item = self.lista_de_request._lista_de_request.item(item_id)            
            
            text = item["text"]

            tree_data.append({
                "id": item_id,
                "text": text,
                "method": method
            })
       
        save_config_data(tree_data)


    def load_data_config(self):
        tree_data = load_treeview_data()
        for item in tree_data:
            text = item['text']
            method= item['method']
            tree_item_id = item['id']
            
            self.lista_de_request._lista_de_request.insert(
                "", "end",
                iid=tree_item_id,
                text=text,
                image=self.pointer_icon
            )            
            # self.tab_mapping['ID'] = tree_item_id
            self.update_notebook(method=method, text=text, tree_item_id=tree_item_id)
            


    def maximize(self):
        self.state('zoomed')

if __name__ == "__main__":
    app = App()
    app.title("App")
    app.mainloop()