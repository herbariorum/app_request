import json  # Certifique-se de importar o módulo JSON
from pathlib import Path


FILE_PATH = Path(__file__).parent.parent


def save_config_data(tree_data, file_path=f"{FILE_PATH}/config_data.json"):
    """Salva os dados do Treeview em um arquivo JSON."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(tree_data, file, indent=4, ensure_ascii=False)
        print(f"Dados salvos com sucesso em {file_path}")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

def load_treeview_data(file_path=f"{FILE_PATH}/config_data.json"):
    """Carrega os dados do Treeview de um arquivo JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado. Nenhum dado carregado.")
        return []
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return []
    
def load_treeview_data_by_id(id, file_path=f"{FILE_PATH}/config_data.json"):
    """Carrega os dados do Treeview de um arquivo JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                if item['id'] == id:
                    return item
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado. Nenhum dado carregado.")
        return []
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return []