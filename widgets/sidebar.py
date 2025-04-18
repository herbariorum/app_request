import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import ImageTk, Image

from idlelib.tooltip import Hovertip
from util.save_data import load_treeview_data_by_id
from util.functions import load_image

notebook = None


class Sidebar():
    def __init__(self, parent, main_app):
        
        self.popup_menu = None   
        self.parent = parent
        self.main_app = main_app

        # self.plus_img = tk.PhotoImage(file=IMG_PATH/'172525_plus_icon.png', height=24, width=24)
        # self.pointer_icon = ImageTk.PhotoImage(Image.open(IMG_PATH/'6637787_direction_menu_point_pointer_icon.png').resize((16, 16)))
        
        self.plus_img = load_image('172525_plus_icon.png', size=(24, 24))
        self.pointer_icon = load_image('6637787_direction_menu_point_pointer_icon.png', size=(16, 16))

        # Inicio os componentes
        self.init_components()

        # self.load_data_config()

    @property
    def tree_request(self):
        return self._lista_de_request

    def init_components(self):
        self.parent.grid_columnconfigure(0, weight=1)

        self.parent.grid_rowconfigure(0, weight=0)
        self.parent.grid_rowconfigure(1, weight=1)

        # Cria uma frame no topo da sidebar
        top_frame = ttk.Frame(
            self.parent,
            height=50,
        )
        
        top_frame.grid(row=0, column=0, sticky='nsew', pady=10)

        button_add = ttk.Button(
            top_frame,
            image=self.plus_img,
            style='Primary.TButton',
            command=self.add_http_request_to_treeview
        )
        button_add.pack(side='right', fill='x', padx=10, pady=10)
        
        Hovertip(button_add, "Inserir novo HTTP Request")

        bottom_frame = ttk.Frame(
            self.parent,      
        )
       
        bottom_frame.grid(row=1, column=0, sticky='nsew', pady=10)

        # Cria a Treeview com o seu Scrollbar
        scrollbar = ttk.Scrollbar(bottom_frame)
        self._lista_de_request = ttk.Treeview(
            bottom_frame, 
            show='tree', 
            yscrollcommand=scrollbar.set,          
            cursor='hand2',
            columns=[1]
            )
  
        scrollbar.configure(command=self._lista_de_request.yview)

        scrollbar.pack(side='right', fill='y')
        self._lista_de_request.pack(side='left', fill='both', expand=True)
        self._lista_de_request.bind("<Double-1>", self.on_treeview_item_click)


        # Cria o menu popup para os items do Treeview
        self.popup_menu = tk.Menu(self._lista_de_request, tearoff=0, font=('Arial', 14))
        self.popup_menu.add_command(label='Rename', command=self.rename_item)
        self.popup_menu.add_command(label='Delete', command=self.delete_item)
        # Associa o evento de clique com o botão direito ao treeview
        self._lista_de_request.bind("<Button-3>", self.show_popup_menu)
    
    
    def on_treeview_item_click(self, event):
        select_item = self._lista_de_request.selection()
        mapping = self.main_app.tab_mapping
        
        if select_item:
            item_id = select_item[0]
            if item_id in mapping:
               
                tab_id = mapping[item_id]
                self.main_app.config_notebook.note.select(tab_id)
            else:
                
                data = load_treeview_data_by_id(select_item[0])
                self.main_app.update_notebook(method=data['method'], text=data['text'], tree_item_id=data['id'])
         

    def add_http_request_to_treeview(self):
        """
        Adiciona um novo item ao Treeview e cria uma aba correspondente no Notebook.
        """
        default_method = "GET"
        tree_item_id = self._lista_de_request.insert("", "end", text="Http Request", image=self.pointer_icon, values=(default_method))
        tab_id = self.main_app.update_notebook(method=default_method, text="Http Request", tree_item_id=tree_item_id)
        self.main_app.tab_mapping[tree_item_id] = tab_id
        self.main_app.save_data_config()


    
    def show_popup_menu(self, event):
        try:
            item_id = self._lista_de_request.identify_row(event.y)
            self._lista_de_request.selection_set(item_id)
            self.popup_menu.post(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def rename_item(self):
        selected_item = self._lista_de_request.selection()
        if selected_item:
            item_id = selected_item[0]
            valor_atual = self._lista_de_request.item(item_id, "text")
            janela_renomear = tk.Toplevel(self.main_app)
            frame = ttk.Frame(janela_renomear, padding=20)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure((0, 1), weight=1, pad=5)

            frame.pack()

            janela_renomear.title("Renomear")

            entry_novo_nome = ttk.Entry(frame)
            entry_novo_nome.insert(0, valor_atual)
            entry_novo_nome.grid(row=0, column=0, sticky='ew', padx=2, pady=2)

            def confirmar_renomeacao():
                novo_nome = entry_novo_nome.get()
                # Atualiza a lista no TreeView
                self._lista_de_request.item(item_id, text=novo_nome)
                
                # Atualiza a aba do notebook
                if item_id in self.main_app.tab_mapping:   
                    tab_id = self.main_app.tab_mapping[item_id]
                    if tab_id in self.main_app.config_notebook.note.tabs():
                        self.main_app.config_notebook.note.tab(tab_id, text=novo_nome)  
                    else:
                        print(f" Tab ID {tab_id} não encontrado no Notebook")

                self.main_app.save_data_config()
                janela_renomear.destroy()
            
            botao_confirmar = ttk.Button(frame, text="Confirmar", command=confirmar_renomeacao, style="Success.TButton")
            botao_confirmar.grid(row=1, column=0, sticky='ew', padx=2, pady=2)

    def delete_item(self):
        """
        Remove o item selecionado do Treeview e a aba correspondente no Notebook.
        """
        selected_item = self._lista_de_request.selection()
        if selected_item:
            item_id = selected_item[0]

            # Remove a aba correspondente no Notebook
            if item_id in self.main_app.tab_mapping:
                tab_id = self.main_app.tab_mapping[item_id]
                if tab_id in self.main_app.config_notebook.note.tabs():
                    self.main_app.config_notebook.note.forget(tab_id)
                del self.main_app.tab_mapping[item_id]

            # Remove o item do Treeview
            self._lista_de_request.delete(item_id)

            # Salva as alterações no arquivo
            self.main_app.save_data_config()
            
    
    def get_lista_de_request(self):
        return self._lista_de_request

    