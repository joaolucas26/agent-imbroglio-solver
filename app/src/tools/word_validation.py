import json
from smolagents import tool

from ..utils.prompt_manager import fill_prompt, load_prompts
from ..utils.client_utils import load_client, load_config


@tool
def evaluate_words_ai(words_to_validate: list, new_instructions: str = "") -> dict:
    """
    Evaluates a list of words using a specialized AI language model to determine its validity for a word game.
    The list must contain more than 50 words for evaluation.

    Args:
        words_to_validate (list): A list of words to be evaluated.
        new_instructions (str, optional): Additional instructions to guide the AI's evaluation. Defaults to an empty string.

    Returns:
        dict: A dictionary with keys "veredito" (verdict) and "justificativa" (justification), or an error message if validation fails.
    """

    if len(words_to_validate) <= 50:
        raise ValueError(
            "A lista de palavras para validação deve conter mais de 50 palavras para avaliação pela IA."
        )

    if not words_to_validate:
        raise ValueError("A lista de palavras para validação está vazia.")

    word_prompt = fill_prompt(
        load_prompts("validation_prompt"),
        words=words_to_validate,
        new_instructions=new_instructions,
    )

    client = load_client()
    config = load_config()

    model_config = config.get("model", {})
    model_name = model_config.get("validation_model_id")
    generation_config = model_config.get("generation_config", {})

    try:
        response = client.models.generate_content(
            model=model_name, contents=word_prompt, config=generation_config
        )

        cleaned_text = response.text.strip()

        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]

        cleaned_text = cleaned_text.strip()

        result_json = json.loads(cleaned_text)

        if (
            not isinstance(result_json, dict)
            or "veredito" not in result_json
            or "justificativa" not in result_json
        ):
            raise ValueError(
                "Resposta da IA não contém os campos esperados 'veredito' e 'justificativa'."
            )

        valid_verdicts = ["VALIDA", "INVALIDA", "DUVIDA"]
        if result_json["veredito"] not in valid_verdicts:
            raise ValueError(
                f"Veredito inválido retornado pela IA: {result_json['veredito']}"
            )

        return result_json

    except json.JSONDecodeError as e:
        raise ValueError("Resposta da IA não é um JSON válido.")
    except Exception as e:

        raise RuntimeError(f"Erro ao avaliar palavras com IA: {str(e)}")


@tool
def evaluate_words_human(words_to_evaluate: str) -> dict:
    """
    Placeholder function for human evaluation of words.

    Args:
        words_to_evaluate (str): A string containing words to be evaluated.
    Returns:
        str: A message indicating that human evaluation is required.
    """

    print("Palavras para avaliação humana:", words_to_evaluate)
    human_answer = input("Por favor, insira o veredito (VALIDA, INVALIDA, DUVIDA): ")
    return {
        "veredito": human_answer,
        "justificativa": "Avaliação realizada por humano.",
    }
