from typing import List, Tuple, Iterator
from math import log2
import itertools
import re
from functools import wraps
import time

LETTER_NOT_IN_WORD = -1
LETTER_IN_WRONG_POSITION = 0
LETTER_IN_RIGHT_POSITION = 1


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


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


def get_regex_from_word_pattern(word: str, pattern: Tuple[int]) -> str:
    """Transform word and its pattern to regex expression

    Args:
        word (str): Word that player write
        pattern (Tuple[int]): tuple with colors of letter:
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
    new_word_list = list(filter(regex_pattern.match, old_word_list))
    return len(new_word_list) / len(old_word_list)


def get_word_patterns(word_length: int = 5) -> Iterator[Tuple[int]]:
    """Return all possible word patterns

    Args:
        word_length (int, optional): Length of word in current game difficulty. Defaults to 5.

    Yields:
        Iterator[Tuple[int]]: words patterns
    """
    possible_colors = [
        LETTER_NOT_IN_WORD,
        LETTER_IN_WRONG_POSITION,
        LETTER_IN_RIGHT_POSITION,
    ]
    return itertools.product(possible_colors, repeat=word_length)


def get_entropy_of_word(word: str, old_word_list: List[str]) -> float:
    """Calculate entropy of word for current word list

    Args:
        word (str): Word that player write
        old_word_list (List[str]):  Current words list of possible answers

    Returns:
        float: Entropy of word for current word list
    """
    word = word.upper()
    entropy_value = 0
    for pattern in get_word_patterns(len(word)):
        regex_expression = get_regex_from_word_pattern(word=word, pattern=pattern)
        probability = get_probabilty_of_word_pattern(
            word, regex_expression, old_word_list
        )
        entropy_value += probability * get_information_value(probability)
    return entropy_value
