from typing import List, Tuple, Dict
from heapq import nlargest
import functions as F
from datetime import datetime as dt
import time
from multiprocessing import Pool as ThreadPool


class Wordle:
    def __init__(self, word_list: List[str]) -> None:
        self.old_word_list: List[str] = word_list
        self.new_word_list: List[str] = []
        self.entropy_list: List[Tuple[str, float]] = []
        self.entropy_dictionary: Dict[str, float] = {}

    def get_entropy_list(self, custom_word_list: List[str] = None):
        word_list = custom_word_list if custom_word_list else self.old_word_list
        for index, word in enumerate(word_list):
            # percentage = index * 100 / len(self.old_word_list)
            # print(word, len(word_list))
            entropy = F.get_entropy_of_word(word, self.old_word_list)
            self.entropy_list.append((word, entropy))
            self.entropy_dictionary[word] = entropy

    def get_word_entory(self, word: str):
        self.entropy_list.append(
            (word, F.get_entropy_of_word(word, self.old_word_list))
        )

    def get_top_10(
        self, new_word_list_entropy: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        top_10 = nlargest(10, new_word_list_entropy, key=lambda x: x[1])
        return top_10


@F.timeit
def pool_test(size: int = 20):
    with open("scratch_main_logic/allowed_words.txt") as file:
        word_list = [word[:-1].upper() for word in file]
    pool = ThreadPool()
    wordle = Wordle(word_list)
    pool.map(wordle.get_word_entory, word_list[:size])
    # print(wordle.entropy_list)


@F.timeit
def single_test(size: int = 20):
    with open("scratch_main_logic/allowed_words.txt") as file:
        word_list = [word[:-1].upper() for word in file]
    wordle = Wordle(word_list)
    wordle.get_entropy_list(custom_word_list=word_list[:size])
    # print(wordle.entropy_list)


@F.timeit
def tuple_list_test():
    with open("scratch_main_logic/allowed_words.txt") as file:
        word_list = [word[:-1].upper() for word in file]
    for i in range(100):
        F.get_entropy_of_word("WEARY", word_list)


def main():
    words_patterns = {}
    with open("scratch_main_logic/allowed_words.txt") as file:
        word_list = [word[:-1].upper() for word in file]
    for word in word_list[:10]:
        word = word.upper()
        for pattern in F.get_word_patterns(len(word)):
            regex_expression = F.get_regex_from_word_pattern(word=word, pattern=pattern)
            if not F.get_probabilty_of_word_pattern(word, regex_expression, word_list):
                words_patterns[word] = words_patterns.get(word, list())
                words_patterns[word].append(pattern)
    # print(words_patterns)


if __name__ == "__main__":
    main()
