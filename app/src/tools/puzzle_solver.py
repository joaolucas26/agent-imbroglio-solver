import json
from typing import List, Dict, Set, Tuple
import time
from smolagents import tool
from ..utils.word_utils import can_form_word
from pathlib import Path


def calculate_solution_score(solution_words: List[Dict]) -> int:
    """Calcula o score de uma solução usando as palavras normalizadas"""
    scores = [len(word["normalized"]) ** 2 for word in solution_words]
    total = sum(scores)
    return total


def find_possible_words(letters):
    """Finds all possible words that can be formed with the given letters.
    Args:
        letters (list): A list of available letters.
        words_data (list): A list of word objects with 'word' and 'normalized' keys.
    Returns:
        list: A list of possible word objects that can be formed."""

    words_path = Path(__file__).parent / "../data/all_words.json"

    with open(words_path, "r", encoding="utf-8") as f:
        words_data = json.load(f)
    possible_words = []
    for word_obj in words_data:
        if can_form_word(letters, word_obj["normalized"]):
            possible_words.append(word_obj)
    possible_words.sort(key=lambda x: (-len(x["word"]), x["word"]))

    return possible_words


@tool
def find_solutions(puzzle_letters: list[str]) -> List[List[Dict]]:
    """Encontra soluções para um puzzle usando as palavras já mapeadas
    Args:
        puzzle_letters: List[str] com as letras do puzzle
    returns: List[List[Dict]] com as melhores soluções encontradas
    """

    max_words = 3
    time_limit = 7.0
    max_solutions = 1000
    best_solutions = 30
    start_time = time.time()

    possible_words = find_possible_words(puzzle_letters)

    solutions = []
    used_solutions = set()

    def try_combinations(
        remaining_letters: List[str], current_solution: List[Dict]
    ) -> None:

        if time.time() - start_time > time_limit:
            return

        if not remaining_letters:
            # Verifica se a solução é única
            solution_key = tuple(
                sorted(word["normalized"] for word in current_solution)
            )
            if solution_key not in used_solutions:
                solutions.append(current_solution.copy())
                used_solutions.add(solution_key)
            return

        if len(current_solution) >= max_words:
            return

        for word in possible_words:
            if can_form_word(remaining_letters, word["normalized"]):
                new_remaining = remaining_letters.copy()
                for letter in word["normalized"]:
                    new_remaining.remove(letter)

                current_solution.append(word)
                try_combinations(new_remaining, current_solution)
                current_solution.pop()

                if len(solutions) >= max_solutions:
                    return

    try_combinations(remaining_letters=puzzle_letters, current_solution=[])

    # Ordena as soluções pelo score
    solutions.sort(key=calculate_solution_score, reverse=True)

    return solutions[:best_solutions]
