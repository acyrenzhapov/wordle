from typing import List
from math import log2


LETTER_NOT_IN_WORD = -1
LETTER_IN_WRONG_POSITION = 0
LETTER_IN_RIGHT_POSITION = 1


def get_bit_value(new_word_list: List[str], old_word_list: List[str]) -> float:
    """Gives information on how many bits of information a word holds

    Args:
        new_word_list (List[str]): list of words that satisfy pattern of new step
        old_word_list (List[str]): list of words from previous step of game

    Raises:
        Exception: new_word_list shouldn't be empty
        Exception: old_word_list shouldn't be empty

    Returns:
        float: bit value of word
    """
    if not new_word_list:
        raise Exception("List with reduced words shouldn't be empty")
    if not old_word_list:
        raise Exception("List with old words shouldn't be empty")
    return log2(len(old_word_list) / len(new_word_list))


def from_word_pattern_to_regex(word: str, pattern: List[int]) -> str:
    """Transform word and its pattern to regex expression 

    Args:
        word (str): Chosen word
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

    for index in range(len(pattern)):
        if isinstance(regex_letters_list[index], list):
            regex_expression += (
                f'[^{"".join(regex_except_list + regex_letters_list[index])}]'
            )
        elif isinstance(regex_letters_list[index], str):
            regex_expression += regex_letters_list[index]
    return regex_expression


print(from_word_pattern_to_regex("STORE", [-1, 0, -1, 1, 0]))
print(log2((3**5)))
print(3 ^ 5)
