from collections import Counter
from smolagents import tool


def can_form_word(letters, word):
    letters_counter = Counter(letters)

    word_counter = Counter(word.lower())
    for letter, count in word_counter.items():
        if letters_counter[letter] < count:
            return False
    return True
