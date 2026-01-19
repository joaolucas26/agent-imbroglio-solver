import os
from smolagents import CodeAgent, LiteLLMModel
import json
from pathlib import Path

from src.utils.prompt_manager import fill_prompt, load_prompts
from src.tools.puzzle_solver import find_solutions
from src.tools.word_validation import evaluate_words_ai, evaluate_words_human
from src.tools.file_handler import (
    load_validated_words,
    save_validated_words,
    # read_json_file,
    rewrite_words_dict,
)


def load_config():
    """Loads the configuration from config.json."""
    config_path = Path(__file__).parent / "src" / "utils" / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    config = load_config()
    model_config = config.get("model", {})

    model = LiteLLMModel(
        model_id=model_config.get("agent_model_id"), api_key=os.getenv("GEMINI_API_KEY")
    )

    agent_instructions = load_prompts("agent_instructions")

    agent = CodeAgent(
        model=model,
        tools=[
            find_solutions,
            evaluate_words_human,
            evaluate_words_ai,
            # read_json_file,
            save_validated_words,
            load_validated_words,
            # rewrite_words_dict
        ],
        additional_authorized_imports=["json", "collections"],
        instructions=agent_instructions,
    )

    daily_letters = [
        "a",
        "a",
        "a",
        "c",
        "g",
        "i",
        "j",
        "l",
        "l",
        "n",
        "o",
        "o",
        "o",
        "o",
        "r",
        "r",
        "t",
    ]

    agent_task = fill_prompt(
        load_prompts("task_prompt"),
        letters=daily_letters,
    )

    final_solutions = agent.run(agent_task)

    print("--- Top Solutions Found by Agent ---")
    print(final_solutions)


if __name__ == "__main__":
    main()
