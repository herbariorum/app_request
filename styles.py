
from tkinter.ttk import Style

def ConfigStyles():
    s = Style()
    s.theme_use('clam')
    # Cores para o botão
    primary_color = "#0d6efd"  # Azul
    p_active_color = "#0b5ed7"    # Azul Claro
    p_disabled_color = "#b0d4ff"  # Azul Claro para desabilitado

    # Cores para o botão Success
    success_color = "#28a745"  # Verde
    success_active_color = "#218838"  # Verde Escuro
    success_disabled_color = "#c3e6cb"  # Verde Claro

    # Cores para o botão Warning
    warning_color = "#ffc107"  # Amarelo
    warning_active_color = "#e0a800"  # Amarelo Escuro
    warning_disabled_color = "#ffeeba"  # Amarelo Claro


    s.configure("TFrame", background= '#2e2e2e')
    s.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
    s.configure("TPanedwindow", background="#2e2e2e", foreground="#ffffff" )
    s.configure("TNotebook", background="#2e2e2e")
    
    s.configure("Primary.TButton",
                foreground="#ffffff",
                background=primary_color,
                font=("Arial", 12),
                padding=5,
                borderwidth=1,
                relief="flat")
    s.map("Primary.TButton",
          background=[("active", p_active_color), ("disabled", p_disabled_color)],
          relief=[("pressed", "sunken"), ("!pressed", "flat")])
    
    s.configure("Success.TButton",
                foreground="#ffffff",
                background=success_color,
                font=("Arial", 12),
                padding=5,
                borderwidth=1,
                relief="flat"
                )
    s.map("Success.TButton",
          background=[("active", success_active_color), ("disabled", success_disabled_color)],
          relief=[("pressed", "sunken"), ("!pressed", "flat")])


    s.configure("Warning.TButton",
                foreground="#ffffff",
                background=warning_color,
                font=("Arial", 12),
                padding=5,
                borderwidth=1,
                relief="flat"
                )
    s.map("Warning.TButton",
          background=[("active", warning_active_color), ("disabled", warning_disabled_color)],
          relief=[("pressed", "sunken"), ("!pressed", "flat")])
    
    # Estilo para o Treeview
    s.configure("Treeview",
                background="#3c3c3c",
                foreground="#ffffff",
                fieldbackground="#4e4e4e",
                rowheight=25)  # Ajuste a altura da linha se necessário
    s.configure("Treeview.Heading",
                background="#2e2e2e",
                foreground="#ffffff",
                font=("Arial", 12, "bold")
                
                )

    # Estilo para o Scrollbar
    s.configure("TScrollbar",
                gripcolor="#4e4e4e",
                background="#3c3c3c",
                troughcolor="#2e2e2e",
                arrowcolor="#ffffff")

    
    s.configure("TEntry",
                fieldbackground="#343a40",  # Cor de fundo
                foreground="#ffffff",        # Cor do texto
                bordercolor="#495057",       # Cor da borda
                relief="flat")               # Estilo da borda