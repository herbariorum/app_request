import tkinter as tk
from tkinter import ttk
from widgets.entrywithplaceholder import EntryWithPlaceholder


from widgets.tab_note_body import TabnoteBody
from widgets.tab_note_headers import TabnoteHeaders


class TabModel:
    def __init__(self, parent, main_app, data=None, validar_url_callback=None):
        """
        Inicializa o modelo de aba.
        :param parent: O widget pai (geralmente o Notebook).
        :param data: Dados específicos para a aba.
        """
        self.parent = parent
        self.main_app = main_app
        self.validar_url_callback = validar_url_callback
        self.frame_host = None
        self.host_entry = None
        self.button_send = None
        self.menuMethods = None
        self.frame = ttk.Frame(parent)  # Frame principal da aba        
        self.data = data or {}
        self.padding = {'padx': 10, 'pady': 10}
        self.var_option_methods = tk.StringVar(value=self.data.get('method', 'GET'))
        self.var_host = tk.StringVar()
       
        self.methods = ['GET','POST','PUT','DELETE','PATCH']

        # Adicione widgets ou layouts específicos aqui
        self.init_components()

    def init_components(self):
        self.frame_top()
        self.frame_content()
            
    def frame_top(self):
        # Cria a frame superior onde irão OptionMenu, Entre e Button
        self.frame_host = ttk.Frame(self.frame)
        self.frame_host.pack(side='top', fill='x', **self.padding )

        self.frame_host.grid_columnconfigure(0, weight=0)
        self.frame_host.grid_columnconfigure(1, weight=1)
        self.frame_host.grid_columnconfigure(2, weight=0)

        self.frame_host.grid_rowconfigure(0, weight=1)
        
        # self.var_option_methods.set(self.data['method'])
        
        self.menuMethods = ttk.OptionMenu(
            self.frame_host,
            self.var_option_methods,
            self.var_option_methods.get(),
            *self.methods,
            command=self.atualiza_arquivo ,     
        )
        self.menuMethods.grid(row=0, column=0, padx=5, pady=5, sticky="w")
      
        self.host_entry = EntryWithPlaceholder(
            self.frame_host,
            placeholder="http://localhost:3000",
            
        )
        self.host_entry.grid(row=0, column=1,  sticky="nsew", pady=5)

        self.button_send = ttk.Button(
            self.frame_host,
            text="SEND",
            style='Success.TButton',
            command=self.on_send_click
        )
        self.button_send.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
    
    def frame_content(self):        
        frame_content = ttk.Frame(self.frame)
        frame_content.pack(fill='both', expand=True, side='bottom', **self.padding)

        # Cria o Notebook com Body e Headers
        self.note_config = ttk.Notebook(frame_content)
        self.note_config.pack(fill='both', expand=True)

        self.body_tab = TabnoteBody(self.note_config)
        self.headers_tab = TabnoteHeaders(self.note_config)

        self.note_config.add(self.body_tab.frame, text="Body")
        self.note_config.add(self.headers_tab.frame, text="Headers")

    def atualiza_arquivo(self, event):        
        novo_metodo = self.var_option_methods.get()
        self.data['method'] = novo_metodo

        tree_item_id = self.data.get('id')
        if tree_item_id:
            self.main_app.lista_de_request.get_lista_de_request().item(
                tree_item_id, values=(novo_metodo,)
            )
        self.main_app.save_data_config()

    
    def on_send_click(self):
        url = self.host_entry.get().strip()
        body_content = self.body_tab.get_text_area_content()
        header_content = self.headers_tab.get_headers_content()
        method = self.get_option_menu_value()

        if self.validar_url_callback:
            self.validar_url_callback(url, method, body_content, header_content)
        

    def get_option_menu_value(self):
        """
        Retorna o valor selecionado no OptionMenu.
        """
        value = self.var_option_methods.get()       
     
        return value
