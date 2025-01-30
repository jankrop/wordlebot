from __main__ import get_best_guess
from utils import get_hints

with open('words.txt', 'r') as f:
    words = f.read().split()

with open('answers.txt', 'r') as f:
    answers_original = f.read().split()

scores = []
failures = 0

for i, answer in enumerate(answers_original):
    answers = answers_original

    print(f'\rGame {i}/{len(answers)}', end='')

    fail = True

    for attempt in range(6):
        if attempt == 0:
            best_guess = 'roate'
        else:
            best_guess = get_best_guess(words, answers)
        hints = get_hints(best_guess, answer)
        # print(best_guess, *hints)
        answers = [a for a in answers if get_hints(best_guess, a) == hints]
        # print(answers)
        if hints == (2, 2, 2, 2, 2):
            fail = False
            scores.append(attempt)
            break

    if fail:
        failures += 1

print()
print(round((len(words) - failures) / len(words) * 100, 2), '% success rate', sep='')
print('Average number of guesses: ', round(sum(scores) / len(words), 2))
for i in range(6):
    if i == 0:
        print('1 guess:   ', end='')
    else:
        print(f'{i+1} guesses: ', end='')
    print(scores.count(i))
