from typing import Tuple
from time import time


class Colors:
    GREEN = 32
    YELLOW = 33
    GRAY = 90
    RED = 91
    WHITE = 97


class LetterHints:
    GRAY = 0
    YELLOW = 1
    GREEN = 2

    COLORS = {
        GRAY: Colors.GRAY,
        YELLOW: Colors.YELLOW,
        GREEN: Colors.GREEN,
    }


class Spinner:
    """A class representing a spinner, keeping track of its state"""
    STATES = ['\u280b', '\u2819', '\u2838', '\u2834', '\u2825', '\u2807']  # Spinner made of Braille characters

    def __init__(self):
        self.start_time = time()

    def get_state(self):
        return (time() - self.start_time) % len(self.STATES)



def color_print(text: str, bg: int = None, fg: int = None, italic: bool = False, end: str = '\n'):
    """Function to print a string to the console with a foreground and background color."""
    if fg is not None and not (30 <= fg <= 37 or 90 <= fg <= 97):
        raise ValueError(f'Invalid foreground color: {fg}')
    if bg is not None and not (30 <= bg <= 37 or 90 <= bg <= 97):
        raise ValueError(f'Invalid background color: {bg}')

    if bg is not None:
        bg += 10  # Background color IDs are always larger by 10 from their foreground counterparts.

    params = []

    if fg:
        params.append(str(fg))
    if bg:
        params.append(str(bg))
    if italic:
        params.append('3')

    print('\033[' + ';'.join(params) + 'm' + text + '\033[0m', end=end)


def print_word_with_hints(text: str, hints: tuple[int, ...]):
    """Function to print a guess word with hints regarding its letters."""
    if len(text) != len(hints):
        raise ValueError(f'Length difference between word and hints: "{text}", {hints}')

    for i in range(len(text)):
        color = LetterHints.COLORS[hints[i]]

        if i == 0:
            color_print('\u2590', fg=color, end='')
        else:
            color_print('\u258c', fg=LetterHints.COLORS[hints[i - 1]], bg=color, end='')

        color_print(text[i].upper(), bg=color, end='')

        if i == len(text) - 1:
            color_print('\u258c', fg=color, end='')



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
        elif guess[:i].count(c) > correct.count(c) - [x for j, x in enumerate(guess) if guess[j] == correct[j]].count(c):
            hints.append(LetterHints.GRAY)  # Marks excess repetitions as gray
        else:
            hints.append(LetterHints.YELLOW)

    return tuple(hints)

