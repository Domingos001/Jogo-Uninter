
import sys
import os

def resource_path(relative_path):
    """
    Obtém o caminho absoluto para um recurso (imagem, som, etc.).
    Esta função é crucial para que o executável (.exe) encontre os arquivos de assets.
    """
    try:
        # Quando o PyInstaller cria o .exe, ele cria uma pasta temporária
        # e guarda o caminho para essa pasta na variável especial _MEIPASS do sys.
        base_path = sys._MEIPASS
    except Exception:

        base_path = os.path.abspath(".")


    return os.path.join(base_path, relative_path)