import tkinter as tk


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # Obter o item sob o mouse
        row_id = self.widget.identify_row(event.y)
        if not row_id:
            return

        # Obter coordenadas do item
        x, y, _, _ = self.widget.bbox(row_id)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Criar a janela do tooltip
        if self.tooltip_window is None:
            self.tooltip_window = tk.Toplevel(self.widget)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", borderwidth=1, relief="solid")
            label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None