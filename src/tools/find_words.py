from pathlib import Path
from data.read_json import read_json
from smolagents import tool
from collections import Counter

@tool
def find_possible_words(letters: list) -> dict:
    """
    Finds all possible words that can be formed from the given list of letters.

    This function is designed for agent or automation use, where the agent provides a list of letters
    and receives all words from the dataset that can be constructed using those letters.

    Args:
        letters (list): A list of single-character strings representing available letters.

    Returns:
        list: A list of word objects (dicts) that can be formed from the given letters, sorted by descending word length and then alphabetically.

    Example:
        possible_words = find_possible_words(['a', 'b', 'c', 'd'])
    """
    words_data = read_json('data/words.json')
    possible_words = []
    
    for word_obj in words_data:
        if can_form_word(letters, word_obj['normalized']):
            possible_words.append(word_obj)
    possible_words.sort(key=lambda x: (-len(x['word']), x['word']))
    
    return possible_words


def can_form_word(letters: list, word: str) -> bool:
    """
    Checks if a word can be formed from the given list of letters.

    This helper function is intended for use by agents to verify if a specific word
    can be constructed using the provided letters, considering letter counts.

    Args:
        letters (list): A list of single-character strings representing available letters.
        word (str): The word to check.

    Returns:
        bool: True if the word can be formed from the letters, False otherwise.

    Example:
        can_form = can_form_word(['a', 'b', 'c'], 'cab')
    """
    letters_counter = Counter(letters)
    
    word_counter = Counter(word.lower())
    for letter, count in word_counter.items():
        if letters_counter[letter] < count:
            return False
    return True