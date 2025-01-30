from .utils import print_word_with_hints, color_print, Colors
from .solver import get_hints, get_best_guess
from . import lists

from importlib import resources
import argparse

def main(answers, fast, find_opener, hard, opener, words):
    if opener: find_opener = False
    if words or answers: find_opener = True

    color_print('\u2590', fg=Colors.GRAY, end='')
    color_print('WordleBot', bg=Colors.GRAY, italic=True, end='')
    color_print('\u258c', fg=Colors.GRAY)

    if hard:
        color_print('\u2590', fg=Colors.GRAY, end='')
        color_print('Hard mode', bg=Colors.GRAY, fg=Colors.RED, end='')
        color_print('\u258c', fg=Colors.GRAY)

    if words:
        with open(words, 'r') as words:
            words = words.read().split()
    else:
        words_file = resources.files(lists) / ('answers.txt' if fast else 'words.txt')
        with words_file.open('r') as f:
            words = f.read().split()

    if answers:
        with open(answers, 'r') as answers:
            answers = answers.read().split()
    else:
        answers_file = resources.files(lists) / 'answers.txt'
        with answers_file.open('r') as f:
            answers = f.read().split()

    hints = ()

    green_letters = {}
    yellow_letters = []

    for attempt in range(6):
        print('Thinking...')

        if hard and attempt != 0:
            new_words = []
            for word in words:
                valid_guess = True
                for i, c in enumerate(word):
                    if green_letters.get(i) and green_letters.get(i) != c:
                        valid_guess = False
                        break
                for c in yellow_letters:
                    if c not in word:
                        valid_guess = False
                        break
                if valid_guess:
                    new_words.append(word)

            words = new_words


        if hints or find_opener:
            best_guess = get_best_guess(words, answers)
        else:
            best_guess = opener or 'roate'  # Pre-calculated using the get_best_guess function

        if len(answers) == 1:
            print('\033[F\033[2K', end='')
            print_word_with_hints(best_guess, (2, 2, 2, 2, 2))
            print()
            break

        print('\033[F\033[2K', *best_guess.upper(), '', sep=' ')

        color_print('Enter word hints like this:', fg=Colors.GREEN, end='')
        print_word_with_hints('012', (0, 1, 2))
        color_print('or "q" to quit', fg=Colors.GREEN)
        result = input('\033[32m>>> ')
        if result == 'q':
            break
        hints = tuple((int(x) for x in result if x.isdigit()))

        for i, c in enumerate(best_guess):
            if hints[i] == 2:
                green_letters[i] = c
            elif hints[i] == 1:
                yellow_letters.append(c)

        answers = [a for a in answers if get_hints(best_guess, a) == hints]

        print('\033[0m\033[2K\033[F\033[2K\033[F\033[2K\033[F\033[2K\033[F')
        print_word_with_hints(best_guess, hints)
        print(len(answers))

        if hints == (2, 2, 2, 2, 2):
            break

        if attempt == 6:
            print('Game failed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='wordle', description='A bot for optimally solving Wordle')

    parser.add_argument('-a', '--answers', metavar='PATH', help='Custom answers file')
    parser.add_argument('-f', '--fast', action='store_true', help='Fast mode: only guess possible answers')
    parser.add_argument('-F', '--find-opener', action='store_true', help='Calculate best opening word, only with -a or -w, exclusive with -o')
    parser.add_argument('-H', '--hard', action='store_true', help='Hard mode')
    parser.add_argument('-o', '--opener', metavar='WORD', help='Custom opening word, exclusive with -F')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-w', '--words', metavar='PATH', help='Custom words file')

    args = parser.parse_args()
    main(**vars(args))

