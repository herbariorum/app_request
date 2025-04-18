from tkinter import ttk, messagebox
import tkinter as tk
from pathlib import Path
from PIL import ImageTk, Image
from urllib.parse import urlparse
import json

from styles import ConfigStyles
from widgets.sidebar import Sidebar
from widgets.notebook import NotebookRequest
from widgets.tab_mode import TabModel

from util.save_data import save_config_data, load_treeview_data
from util.functions import process_tab_data
from util.functions import load_image
from util.save_data import save_data, load_data


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ConfigStyles()  # Certifique-se de chamar isso aqui
       
        self.lista_de_request = None
        self.frame_do_meio = None
        self.frame_da_direita = None
        self.tab_mapping = {}

       
        self.pointer_icon = load_image('6637787_direction_menu_point_pointer_icon.png',size=(16, 16) )

        self.after(100, self.maximize)

        painelprincipal = tk.PanedWindow(
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
        painelprincipal.pack(expand=True, fill='both')

        painelprincipal.grid_columnconfigure(0, weight=0) # coluna não expande
        painelprincipal.grid_columnconfigure((1, 2), weight=1) # colunas podem expandir
        painelprincipal.grid_rowconfigure(0, weight=1) # linha expande

        # Painel de Exibição dos Requests em um treeview
        self.frame_sidebar = ttk.Frame(painelprincipal, border=1, borderwidth=2)

        # Cria a Sidebar
        self.lista_de_request = Sidebar(self.frame_sidebar, self)
        # self.lista_de_request._lista_de_request.bind("<Double-1>", self.update_notebook)
        
        # Painel de Edição/Configuração dos Requests
        self.frame_do_meio = ttk.Frame(painelprincipal, width=740, border=1, borderwidth=2)
        
        self.config_notebook = NotebookRequest(self.frame_do_meio, self)

        # Painel de Resultados dos Requests
        self.frame_da_direita = ttk.Frame(painelprincipal)
        
        # Exibe os frames
        self.frame_sidebar.grid(row=0, column=0, sticky='ns')
        self.frame_do_meio.grid(row=0, column=1, sticky='nsew')
        self.frame_da_direita.grid(row=0, column=2, sticky='nsew')

        # Adiciona todas as  frames mo PanelWindow
        painelprincipal.add(self.frame_sidebar)
        painelprincipal.add(self.frame_do_meio)
        painelprincipal.add(self.frame_da_direita)

        self.load_data_config()
        self.load_config()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    
    def update_notebook(self, method='GET', text=None, tree_item_id=None):        
        """
        Atualiza ou cria uma aba no Notebook com base no tree_item_id.
        """ 
        if tree_item_id in self.tab_mapping:           
            # Aba já existe, atualiza o texto da aba se necessário
            tab_id = self.tab_mapping[tree_item_id]
            if tab_id in self.config_notebook.note.tabs():
                self.config_notebook.note.tab(tab_id)
                return tab_id
            else:
                print(f"Tab ID {tab_id} não encontrado no Notebook.")
        else:            
             # Cria uma nova aba
            self.tab_model = TabModel(
                self.config_notebook.note, 
                main_app=self, 
                data={"id": tree_item_id, "method": method, "text": text},
                validar_url_callback=self.validar_url
            )
            self.tab_model.frame.tab_model = self.tab_model
            self.config_notebook.note.add(self.tab_model.frame, text=text)
            tab_id = str(self.tab_model.frame)
            # Mapeia o tree_item_id para o novo tab_id
            if tree_item_id:
                self.tab_mapping[tree_item_id] = tab_id  # Corrigido para usar tree_item_id como chave
        return tab_id

    def save_data_config(self):
        tree_data = []
        for item_id in self.lista_de_request.get_lista_de_request().get_children():
            item = self.lista_de_request.get_lista_de_request().item(item_id)
           
            text = item["text"]
            method = item.get("values", ["GET"])[0]

            tree_data.append({
                "id": item_id,
                "text": text,
                "method": method
            })       
        save_config_data(tree_data)
       
    def load_data_config(self):
        tree_data = load_treeview_data()
        print(tree_data)
        for item in tree_data:
            text = item['text']
            method= item['method']
            tree_item_id = item['id']
            
            self.lista_de_request.get_lista_de_request().insert(
                "", "end",
                iid=tree_item_id,
                text=text,
                values=(method),
                image=self.pointer_icon
            )            
            self.tab_mapping['ID'] = tree_item_id
            self.update_notebook(method=method, text=text, tree_item_id=tree_item_id)
    
    def validar_url(self, url, method, body_content, headers_content):                
        if not url:
            messagebox.showerror("Erro", "O campo URL não pode estar vazio.")
            return False
        # Verifica se é uma URL válida
        if not self.is_valid_url(url):
             messagebox.showerror("Erro", "Digite uma url válida")            
             return False
       
        try:
            body_content = json.loads(body_content)
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "O conteúdo do body não é um JSON válido.")
            return False

        json_result = process_tab_data(url, method, body_content, headers_content)
        print(json_result)        
        
        return True
    
    def is_valid_url(self, url):
        """
        Verifica se a URL é válida usando urllib.parse.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    
    # Methodo para salvar os dados ao sair do app
    def on_close(self):
        self.save_config()
        self.destroy()

    def save_config(self): 
        all_data = []
        
        for tab_id in self.lista_de_request.get_lista_de_request().get_children():
            unique_id = tab_id

            # Obtém o tab_model associado à aba
            try:
                tab_frame = self.config_notebook.note.nametowidget(self.tab_mapping[tab_id])
                tab_model = getattr(tab_frame, "tab_model", None)
            except KeyError:
                print(f"Tab ID '{tab_id}' não encontrado no Notebook. Ignorando.")
                continue

            if not tab_model:
                print(f"TabModel não encontrada para a aba {tab_id}")
                continue

            headers = tab_model.headers_tab.get_headers_content()
            body_content = tab_model.body_tab.get_text_area_content()
           
            try:
                body = json.loads(body_content)
            except json.JSONDecodeError:
                body = {}

            all_data.append({    
                "id": unique_id,        
                "headers": headers,
                "body": body
            })
        
        save_data(all_data)            

    def load_config(self):
        all_data = load_data()      
        if not all_data:
            print("Nenhum dado encontrado no arquivo de configuração.")
            return
        
        for tab_data in all_data:
            tab_id = tab_data['id']            

            if tab_id not in self.tab_mapping:
                print(f"Aba com ID '{tab_id}' não encontrada no Notebook principal.")
                continue
            
            tab_frame = self.config_notebook.note.nametowidget(self.tab_mapping[tab_id])
            tab_model = getattr(tab_frame, "tab_model", None)

            if not tab_model:
                print(f"TabModel não encontrado para a aba {tab_id}.")
                continue

            tab_model.headers_tab.limpa_treeview()
            # # Preenche os headers
            for key, value in tab_data["headers"].items():
                tab_model.headers_tab.headers_tree.insert("", "end", values=(key, value))
            
            # # Preenche os body
            tab_model.body_tab.text_area.delete("1.0", "end")
            tab_model.body_tab.text_area.insert("1.0", json.dumps(tab_data["body"], indent=4))

    def maximize(self):
        self.state('zoomed')

if __name__ == "__main__":
    app = App()
    app.title("App")
    app.mainloop()