# configurations.py
from tkinter import PhotoImage
from pathlib import Path


IMG_PATH = Path(__file__).parent.parent / "images"

# Configurações de notificação
img_pad = (5, 0)  # Espaçamento da imagem
text_pad = (5, 0)  # Espaçamento do texto

# Função para carregar imagens
def load_images():
    """
    Carrega as imagens necessárias para o aplicativo.
    Deve ser chamado após a inicialização do Tkinter.
    """
    return {
        "warning": PhotoImage(file=IMG_PATH / "warning_icon.png"),
    }