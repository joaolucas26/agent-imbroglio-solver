import json
from smolagents import tool
import time

from ..utils.prompt_manager import fill_prompt, load_prompts
from ..utils.client_utils import load_client, load_config


@tool
def evaluate_words_ai(
    words_to_validate: list, new_instructions: str = "", batch_size: int = 100
) -> dict:
    """
    Evaluates a list of words using a specialized AI language model to determine its validity for a word game.
    Processes words in batches to handle large lists efficiently.

    Args:
        words_to_validate (list): A list of words to be evaluated.
        new_instructions (str, optional): Additional instructions to guide the AI's evaluation. Defaults to an empty string.
        batch_size (int, optional): Number of words to process in each batch. Defaults to 100.

    Returns:
        dict: A dictionary where each key is a word and the value is another dict with "veredito" and "justificativa".
              Format: {"palavra": {"veredito": "VALIDA/INVALIDA/DUVIDA", "justificativa": "reason"}}
    """

    if not words_to_validate:
        raise ValueError("A lista de palavras para validação está vazia.")

    client = load_client()
    config = load_config()

    model_config = config.get("model", {})
    model_name = model_config.get("validation_model_id")
    generation_config = model_config.get("generation_config", {})

    max_retries = 3
    retry_base_delay = 10

    all_results = {}
    for i in range(0, len(words_to_validate), batch_size):
        batch = words_to_validate[i : i + batch_size]
        print(
            f"Processando lote {i//batch_size + 1}: {len(batch)} palavras (palavras {i+1}-{min(i+batch_size, len(words_to_validate))})"
        )

        word_prompt = fill_prompt(
            load_prompts("validation_prompt"),
            words=batch,
            new_instructions=new_instructions,
        )

        attempt = 0
        while True:
            try:
                response = client.models.generate_content(
                    model=model_name, contents=word_prompt
                )

                try:
                    result_json = json.loads(response.text)
                    if not isinstance(result_json, dict):
                        raise ValueError("Resposta da IA deve ser um dicionário.")

                    all_results.update(result_json)
                    break

                except json.JSONDecodeError as e:
                    print(f"Erro de JSON no lote {i//batch_size + 1}: {str(e)}")
                    for word in batch:
                        all_results[word] = {
                            "veredito": "ERRO",
                            "justificativa": f"Erro no processamento do lote: JSON inválido",
                        }
                    break

            except Exception as e:
                error_message = str(e)
                is_unavailable_503 = (
                    "503 UNAVAILABLE" in error_message
                    and "high demand" in error_message.lower()
                )

                if is_unavailable_503 and attempt < max_retries:
                    attempt += 1
                    wait_time = retry_base_delay * attempt
                    print(
                        f"Lote {i//batch_size + 1}: modelo indisponível (503). Tentativa {attempt}/{max_retries} em {wait_time}s."
                    )
                    time.sleep(wait_time)
                    continue

                print(f"Erro no lote {i//batch_size + 1}: {error_message}")
                for word in batch:
                    all_results[word] = {
                        "veredito": "ERRO",
                        "justificativa": f"Erro na requisição: {error_message}",
                    }
                break

        time.sleep(10)

    if not all_results:
        raise RuntimeError(
            "Nenhum resultado foi obtido durante o processamento em lotes."
        )

    return all_results


@tool
def evaluate_words_human(words_to_evaluate: str) -> dict:
    """
    Placeholder function for human evaluation of words.
    One word at a time should be evaluated by a human, who will provide the verdict
    Call this tool many times you want until all words are you dont know the meaning are evaluated.

    Args:
        words_to_evaluate (str): A string containing words to be evaluated.
    Returns:
        str: A message indicating that human evaluation is required.
    """

    print("Palavras para avaliação humana:", words_to_evaluate)
    human_answer = input("Por favor, insira o veredito (VALIDA, INVALIDA): ")
    return {
        "veredito": human_answer,
        "justificativa": "Avaliação realizada por humano.",
    }
