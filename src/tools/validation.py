
import os
from smolagents import tool
import google.generativeai as genai

from typing import Any


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
MODELO_VALIDACAO = genai.GenerativeModel('gemini/gemini-2.0-flash')

def create_validation_prompt(word: str) -> str:
    prompt_path = os.path.join('data/validation_word_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.replace('{word}', word)
    return prompt


@tool
def evaluate_words_ai(dict_word: dict, model: Any) -> dict:
    """
    Evaluates a word using an AI language model to determine its validity for a word game.

    This function is designed for agent or automation use, where the agent provides a dictionary containing a word
    and a language model instance. The function generates a validation prompt, sends it to the model, and parses the
    model's response to return a structured verdict and justification.

    Args:
        dict_word (dict): A dictionary containing at least the key "word" with the word to be evaluated as a string.
        model: An AI language model instance with a generate_content(prompt) method.

    Returns:
        dict: A dictionary with keys "veredito" (verdict) and "justificativa" (justification), or an error message if validation fails.

    Example:
        result = evaluate_words_ai({"word": "casa"}, model)
    """
    
    if not MODELO_VALIDACAO:
        return {"veredito": "ERRO", "justificativa": "O modelo de IA de validação não pôde ser inicializado."}
    
    palavra_str = dict_word.get("word", "")
    word_prompt = create_validation_prompt(palavra_str)
    
    try:
        # Usa o comando .generate_content() que é específico da biblioteca do Google
        resposta_ia = MODELO_VALIDACAO.generate_content(word_prompt)
        print(f"{palavra_str=}")
        # Acessa a propriedade .text para pegar o resultado
        texto_resposta_limpo = resposta_ia.text.strip().replace("```json", "").replace("```", "")
        print(f"{texto_resposta_limpo=}")
        resultado_json = json.loads(texto_resposta_limpo)
        
        return resultado_json
    
    except Exception as e:
        return {"veredito": "ERRO", "justificativa": f"Falha na validação com a IA: {e}"}
    
def evaluate_words_human(word: str) -> str:
    pass

