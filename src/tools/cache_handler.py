
import json
from pathlib import Path

PATH_ROOT = Path(__file__).resolve().parent.parent.parent
PATH_CACHE = PATH_ROOT / "results" / "ia_validation_cache.json"

def load_cache() -> dict:
    """
    Carrega o cache de validações da IA de um arquivo JSON.
    Se o arquivo não existir, retorna um dicionário vazio.
    """
    try:
        with open(PATH_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(cache_data: dict):
    try:
        with open(PATH_CACHE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"ERRO ao salvar o cache: {e}")