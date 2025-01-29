from utils import LetterHints, Spinner, print_word_with_hints, get_hints, color_print, Colors

import itertools


HARD_MODE = True


def get_best_guess(words: list[str], answers: list[str]):
    """
    Function to find the best guess given a set of words and a set of answers.
    The best guess is the one that on average will create the smallest set of possible answers.
    """
    if len(answers) == 1:
        return answers[0]

    guesses = {}

    # spinner = Spinner()

    for i, guess in enumerate(words):
        hint_answers = {h: 0 for h in itertools.product((0, 1, 2), repeat=5)}

        for answer in answers:
            hints = get_hints(guess, answer)
            if hints != (2, 2, 2, 2, 2):  # For a complete guess the answer set reduces to 0, because we end the game
                hint_answers[hints] += 1

        # score = (hint probability) * (possible answers) = (possible answers)/(all answers) * (possible answers)
        score = sum(h ** 2 for h in hint_answers.values()) / len(answers)

        guesses[guess] = score

        # print(f'\r{round(i/len(words.txt)*100)}%', end='')

    best_guess = min(guesses, key=guesses.get)
    return best_guess

def main():
    color_print('\u2590', fg=Colors.GRAY, end='')
    color_print('WordleBot', bg=Colors.GRAY, italic=True, end='')
    color_print('\u258c', fg=Colors.GRAY)

    if HARD_MODE:
        color_print('\u2590', fg=Colors.GRAY, end='')
        color_print('Hard mode', bg=Colors.GRAY, fg=Colors.RED, end='')
        color_print('\u258c', fg=Colors.GRAY)

    with open('words.txt', 'r') as f:
        words = f.read().split()

    with open('answers.txt', 'r') as f:
        answers = f.read().split()

    hints = ()

    green_letters = {}
    yellow_letters = []

    for attempt in range(6):
        print('Thinking...')

        if HARD_MODE and attempt != 0:
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


        if hints:
            best_guess = get_best_guess(words, answers)
        else:
            best_guess = 'roate'  # Pre-calculated using the get_best_guess function

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
    main()

