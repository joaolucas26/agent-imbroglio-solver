import json
from smolagents import tool


@tool
def load_validated_words(filepath: str) -> dict:
    """Carrega palavras validadas do cache para evitar re-validação.

    Esta função funciona como um cache handler, permitindo que o agente
    verifique quais palavras já foram validadas anteriormente, evitando
    chamadas desnecessárias para ferramentas de validação.

    Args:
        filepath (str): Caminho para o arquivo JSON de cache das palavras validadas

    Returns:
        dict: Dicionário com palavras validadas (chave) e suas informações (valor)
              Format: {"palavra": {"veredito": "VALIDA/INVALIDA/DUVIDA", "justificativa": "reason"}}

    Usage:
        Chame esta função ANTES de validar palavras para verificar se elas
        já estão no cache. Só valide palavras que não estão no dicionário retornado.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            validated_words = json.load(f)
        return validated_words if isinstance(validated_words, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


@tool
def save_validated_words(
    filepath: str, words: dict, merge_with_existing: bool = True
) -> None:
    """Salva palavras validadas no cache para uso futuro, com opção de merge automático.

    Esta função funciona como um cache handler, salvando palavras que foram
    validadas para evitar re-validação em execuções futuras do agente.
    Por padrão, combina automaticamente com palavras já existentes no cache.

    Args:
        filepath (str): Caminho para o arquivo JSON de cache das palavras validadas
        words (dict): Dicionário de palavras validadas com seus vereditos e justificativas
                     Format: {"palavra": {"veredito": "VALIDA/INVALIDA/DUVIDA", "justificativa": "reason"}}
        merge_with_existing (bool): Se True, combina com cache existente. Se False, sobrescreve. Default: True

    Returns:
        None

    Usage:
        Chame esta função APÓS validar novas palavras para adicioná-las ao cache.
        O merge com palavras existentes é feito automaticamente por padrão.
    """
    final_words = words.copy()

    if merge_with_existing:
        existing_cache = load_validated_words(filepath)
        existing_cache.update(final_words)
        final_words = existing_cache

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(final_words, f, ensure_ascii=False, indent=2)

    print(f"Salvo {len(final_words)} palavras validadas em '{filepath}'.")


# @tool
# def read_json_file(file_path: str) -> dict:
#     """
#     Reads a JSON file from the specified path and returns its content as a Python dictionary or list.

#     Args:
#         file_path (str): The absolute or relative path to the JSON file.

#     Returns:
#         dict or list: The parsed content of the JSON file.
#     """

#     with open(file_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     return data


# @tool
def rewrite_words_dict(word_dict_with_invalid_words_removed: list) -> None:
    """
    Use this tool to rewrite the words.json file with the updated list of valid words.
    Every invalid word must be removed from the json before saving.
    IMPORTANT: This function preserves the original ID structure of each word for future reference and deletion.

    Args:
        word_dict_with_invalid_words_removed (list): List of word objects with original structure preserved.
                                                    Format: [{"id": 0, "word": "que", "normalized": "que"}, ...]
    """

    with open("app\\src\\data\\all_words.json", "w", encoding="utf-8") as f:
        json.dump(word_dict_with_invalid_words_removed, f, ensure_ascii=False, indent=4)
