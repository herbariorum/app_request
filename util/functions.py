import json
import requests


# def process_tab_data(url, method, body_content, headers_content):
#     """
#     Processa os dados coletados das abas e retorna um JSON.
#     :param url: A URL validada.
#     :param method: O método HTTP selecionado (GET, POST, etc.).
#     :param body_content: O conteúdo do corpo (Body).
#     :param headers_content: O conteúdo dos cabeçalhos (Headers).
#     :return: Um JSON com os dados processados.
#     """
#     method_map = {
#         "PUT": requests.put,
#         "POST": requests.post,
#         "GET": requests.get,
#         "DELETE": requests.delete,
#         "PATCH": requests.patch
#     }
#     try:
#         if method in method_map:
#             response = method_map[method](url, data=body_content if method in ["PUT", "POST", "PATCH"] else None, headers=headers_content)
#             return response.json()
#         else:
#             raise ValueError("Metodo HTTP não suportado.")

#     except requests.exceptions.RequestException as e:
#         print(f"Erro ao fazer o request: {e}")
#         return None

def process_tab_data(url, method, body_content, headers_content):
    import requests

    try:
        # Faz a requisição HTTP
        response = requests.request(
            method=method,
            url=url,
            json=body_content,
            headers=headers_content
        )

        # Verifica se a resposta é válida
        response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx

        # Tenta interpretar a resposta como JSON
        try:
            return {
                "headers": dict(response.headers),
                "status": response.status_code,
                "data": response.json()  # Tenta interpretar como JSON
            }
        except ValueError:
            return {
                "headers": dict(response.headers),
                "status": response.status_code,
                "data": response.text  # Retorna o texto bruto da resposta
            }

    except requests.exceptions.RequestException as e:
        return {
            "headers": None,
            "status": None,
            "data": None,
            "error": str(e)
        }

from pathlib import Path
from PIL import Image, ImageTk
# Caminho base para as imagens
IMG_PATH = Path(__file__).parent.parent / "images"

def load_image(image_name, size=None):
    """
    Carrega uma imagem a partir do diretório de imagens.
    :param image_name: Nome do arquivo da imagem (ex: "icon.png").
    :return: Objeto PhotoImage da imagem carregada.
    """
    try:
        image_path = IMG_PATH / image_name
        image = Image.open(image_path)
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)

        return ImageTk.PhotoImage(image)
    except Exception as e:
        raise FileNotFoundError(f"Erro ao carregar a imagem '{image_name}': {e}")