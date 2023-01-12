from functions import get_entropy_of_word


def main():
    with open("scratch_main_logic/allowed_words.txt") as file:
        word_list = [word[:-1].upper() for word in file]
    entropy = get_entropy_of_word("WEARY", word_list)
    print(entropy)


if __name__ == "__main__":
    main()
