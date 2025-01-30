import itertools
from .utils import LetterHints


def get_hints(guess: str, correct: str) -> tuple[int, ...]:
    """Functions that calculates hints for a guess"""
    if len(guess) != len(correct):
        raise ValueError(f'Length difference between guess and correct: "{guess}", "{correct}"')

    hints = []

    for i, c in enumerate(guess):
        if c not in correct:
            hints.append(LetterHints.GRAY)
        elif correct[i] == c:
            hints.append(LetterHints.GREEN)
        elif guess[:i].count(c) >= correct.count(c) - [x for j, x in enumerate(guess) if guess[j] == correct[j]].count(c):
            hints.append(LetterHints.GRAY)  # Marks excess repetitions as gray
        else:
            hints.append(LetterHints.YELLOW)

    return tuple(hints)

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