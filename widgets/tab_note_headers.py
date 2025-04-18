import tkinter as tk
from tkinter import ttk
from util.functions import load_image


class TabnoteHeaders(ttk.Frame):
    def __init__(self, parent):
        
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        # self.grid_columnconfigure(0, weight=1)

        # self.grid_rowconfigure(0, weight=0)
        # self.grid_rowconfigure(1, weight=1)
        self.headers_tree = None

        # Carrega a imagem
        self.img_add = load_image("172525_plus_icon.png", size=(16, 16))
        self.img_del = load_image("2849797_trash_icon.png", size=(16, 16))

        self.init_componentes()

    def init_componentes(self):
        # Botões para adicionar ou excluir
        frame_button = ttk.Frame(self.frame)
        frame_button.pack(fill='x', side='top')

        self.button_add = ttk.Button(
            frame_button,
            image=self.img_add,
            command=self.add_header
        )

        self.button_remove = ttk.Button(
            frame_button,
            image=self.img_del,
            command=self.limpa_treeview
        )


        # self.button_add.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.button_add.pack(fill='x', side='left', padx=10, pady=10)
        self.button_remove.pack(fill='x', side='left', padx=10, pady=10)

        # Visualização dos headers
        self.headers_tree = ttk.Treeview(self.frame, columns=("key", "value"), show="headings")
        self.headers_tree.heading("key", text="Key")
        self.headers_tree.heading("value", text="Value")
        # self.headers_tree.grid(row=1, column=0, sticky="nsew")
        self.headers_tree.pack(fill='both', expand=True)

        self.headers_tree.insert("", "end", values=("Content-Type", "application/json"))
        self.headers_tree.bind("<Double-1>", self.start_edit)

        # Adiciona o evento de clique com o botão direito
        self.headers_tree.bind("<Button-3>", self.show_popup_menu)

        # Cria o popup menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Deletar linha", command=self.delete_selected_row)
    
    def show_popup_menu(self, event):
        item_id = self.headers_tree.identify_row(event.y)
        if item_id:
            self.headers_tree.selection_set(item_id)
            self.popup_menu.post(event.x_root, event.y_root)

    def handle_action(self, action):
        if action == "Deletar linha":
            self.delete_selected_row()

    
    def delete_selected_row(self):
        selected_item = self.headers_tree.selection()
        if selected_item:
            self.headers_tree.delete(selected_item)
        

    def add_header(self):
        """
        Adiciona um novo cabeçalho ao Treeview e ativa o modo de edição.
        """        
        item_id = self.headers_tree.insert("", "end", values=("New-Key", "New-Value"))
        # Ativa o modo de edição na primeira célula (Key)
        self.start_edit(event=None, item_id=item_id, column="key")


    def start_edit(self, event=None, item_id=None, column=None):
        """
        Inicia o modo de edição para uma célula do Treeview.
        """
        column_mapping = {"key": 0, "value": 1}

        if event:
            region = self.headers_tree.identify("region", event.x, event.y)
            if region != "cell":
                return  # Apenas permite a edição de células
            column = self.headers_tree.identify_column(event.x)  # Retorna algo como "#1"
            item_id = self.headers_tree.identify_row(event.y)

            column_index = int(column.replace("#", "")) - 1
        else:
            # Se o nome da coluna for passado diretamente (ex: "key" ou "value")
            column_index = column_mapping.get(column, None)
            if column_index is None:
             raise ValueError(f"Coluna inválida: {column}")

        # Obtém os valores atuais do item
        values = self.headers_tree.item(item_id, "values")

        # Cria um Entry temporário para edição
        self.entry_editor = ttk.Entry(self.frame)
        self.entry_editor.insert(0, values[column_index])  # Insere o valor atual
        self.entry_editor.select_range(0, "end")  # Seleciona o texto para edição
        self.entry_editor.focus()

        bbox = self.headers_tree.bbox(item_id, f"#{column_index + 1}")
      
        if bbox:
             # Ajusta o posicionamento do Entry para alinhar corretamente
            x_offset = self.headers_tree.winfo_rootx() - self.frame.winfo_rootx()
            y_offset = self.headers_tree.winfo_rooty() - self.frame.winfo_rooty()
            self.entry_editor.place(
                x=bbox[0] + x_offset, y=bbox[1] + y_offset, width=bbox[2], height=bbox[3]
            )
        
        # Vincula eventos para salvar ou cancelar a edição
        self.entry_editor.bind("<Return>", lambda e: self.save_edit(item_id, column_index))
        self.entry_editor.bind("<Escape>", lambda e: self.cancel_edit())

    def save_edit(self, item_id, column_index):       
        """
        Salva o valor editado no Treeview.
        """
        if not self.entry_editor:
            return  # Garante que o Entry ainda existe
        
        # Obtém o novo valor do Entry
        new_value = self.entry_editor.get()

        # Atualiza o valor no Treeview
        values = list(self.headers_tree.item(item_id, "values"))
        values[column_index] = new_value
        self.headers_tree.item(item_id, values=values)

        # Remove o Entry temporário
        self.entry_editor.destroy()
        self.entry_editor = None

    def cancel_edit(self):
        """
        Cancela a edição e remove o Entry temporário.
        """
        if self.entry_editor:
            self.entry_editor.destroy()
            self.entry_editor = None

    def limpa_treeview(self):
        """
        Remove todos os itens do Treeview.
        """
        for item in self.headers_tree.get_children():
            self.headers_tree.delete(item)

    def get_headers_content(self):
        """
        Retorna os dados dos cabeçalhos como um dicionário.
        """
        headers = {}
        for item_id in self.headers_tree.get_children():
            key, value = self.headers_tree.item(item_id, "values")
            headers[key] = value
        return headers
    
    