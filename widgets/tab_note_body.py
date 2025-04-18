from tkinter import ttk, Text

class TabnoteBody(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.text_area = None
        self.init_componentes()

    def init_componentes(self):                
        self.text_area = Text(self.frame, wrap="word", bg="#2b2b2b", fg="#ffa500", insertbackground="#ffa500")
        self.text_area.tag_configure("default", foreground="#ffa500")
        ys = ttk.Scrollbar(self.frame, orient='vertical', command=self.text_area.yview)
        self.text_area['yscrollcommand'] = ys.set

        self.text_area.grid(row=0, column=0, sticky="nwes")
        ys.grid(row=0, column=1, sticky="ns")

        self.text_area.insert("1.0", "{}", "default")

    def get_text_area_content(self):
        content = self.text_area.get("1.0","end-1c").strip()
        content = content.replace("\n", "")
        return content