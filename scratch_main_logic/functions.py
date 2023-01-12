from typing import List
from math import log2
import itertools
import re

LETTER_NOT_IN_WORD = -1
LETTER_IN_WRONG_POSITION = 0
LETTER_IN_RIGHT_POSITION = 1


def get_information_value(probability: float) -> float:
    """Gives information on how many bits of information a word holds

    Args:
        probability (float): Ration between new_word_list and old_word_list

    Returns:
        float: probabilty of word
    """
    if not probability:
        return 0
    return log2(1 / probability)


def get_regex_from_word_pattern(word: str, pattern: List[int]) -> str:
    """Transform word and its pattern to regex expression

    Args:
        word (str): Word that player write
        pattern (List[int]): list with colors of letter:
            -1 is gray
            0 is yellow/amber
            1 is green

    Returns:
        str: regex expression that describes possible words of chosen word and its pattern
    """
    regex_expression: str = r""
    regex_except_list: List[str] = []
    regex_letters_list: List[List[str]] = [[] for i in range(len(word))]

    for index, (letter, letter_status) in enumerate(zip(word, pattern)):
        if letter_status == LETTER_NOT_IN_WORD:
            regex_except_list.append(letter)
        elif letter_status == LETTER_IN_WRONG_POSITION:
            regex_letters_list[index].append(letter)
        elif letter_status == LETTER_IN_RIGHT_POSITION:
            regex_letters_list[index] = letter
    for item in regex_letters_list:
        if isinstance(item, list) and (len(item) > 0):
            regex_expression += f"(?=.*{item[0]})"

    for index in range(len(pattern)):
        if isinstance(regex_letters_list[index], list):
            regex_expression += (
                f'[^{"".join(regex_except_list + regex_letters_list[index])}]'
            )
        elif isinstance(regex_letters_list[index], str):
            regex_expression += regex_letters_list[index]
    return regex_expression


def get_probabilty_of_word_pattern(
    word: str, regex_expression: str, old_word_list: List[str]
) -> float:
    """Calculate percentage of words that satisfy regex expression to all current words in list

    Args:
        word (str): Word that player write
        regex_expression (str): regex expression that was created by pattern
        old_word_list (List[str]): Current words list of possible answers

    Raises:
        Exception: if word list is empty

    Returns:
        float: probality or percentage of words that satisfy regex expression
    """
    if not old_word_list:
        raise Exception("List with old words shouldn't be empty")
    regex_pattern = re.compile(regex_expression)
    new_word_list: List[str] = []
    for word in old_word_list:
        if regex_pattern.search(word) is not None:
            new_word_list.append(word)
    return len(new_word_list) / len(old_word_list)


def get_entropy_of_word(word: str, old_word_list: List[str]) -> float:
    """Calculate entropy of word for current word list

    Args:
        word (str): Word that player write
        old_word_list (List[str]):  Current words list of possible answers

    Returns:
        float: Entropy of word for current word list
    """
    word = word.upper()
    possible_colors = [
        LETTER_NOT_IN_WORD,
        LETTER_IN_WRONG_POSITION,
        LETTER_IN_RIGHT_POSITION,
    ]
    entropy_value = 0
    for index, pattern in enumerate(
        itertools.product(possible_colors, repeat=len(word))
    ):
        pattern = list(pattern)
        regex_expression = get_regex_from_word_pattern(word=word, pattern=pattern)
        probability = get_probabilty_of_word_pattern(
            word, regex_expression, old_word_list
        )
        entropy_value += probability * get_information_value(probability)
    return entropy_value
