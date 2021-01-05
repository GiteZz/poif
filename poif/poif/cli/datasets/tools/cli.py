from pathlib import Path
from typing import Callable, List, Optional


def simple_input(title: str, default: str = None) -> str:
    if default is not None:
        print(f'{title}: [default: {default}]')
    else:
        print(f'{title}: ')

    return input_with_possible_default(default=default)


def answer_from_list(title: str, answer_list: List[str], default: str = None):
    print(f'{title} Options: {answer_list}')
    return input_with_possible_default(default=default, validation_function=in_list_validation(answer_list))


def path_input(title: str, default: Path = None):
    if default is not None:
        print(f'{title}: [default: {str(default)}]')
    else:
        print(f'{title}: ')

    answer = input_with_possible_default(default=None if default is None else str(default))

    return Path(answer)


def multi_input(title: str, empty_allowed=False):
    print(title + ' [Empty input to stop]')

    answers = []
    while True:
        answer = input()
        if answer != "":
            answers.append(answer)
        else:
            if len(answers) > 0 or empty_allowed:
                return answers
            else:
                print('Please provide one or more answers')


class MaxTriesReachedException(Exception):
    pass


def input_with_possible_default(default=None, validation_function=None) -> str:
    invalid_count = 0
    max_invalid_count = 3
    # Bit arbitrary but avoids infinite loop and allows for better testing
    while invalid_count < max_invalid_count:
        answer = input()

        if validation_function is not None and not validation_function(answer):
            print('Answer was not valid, please provide a correct answer.')
            invalid_count += 1
            continue

        if default is not None and answer == "":
            return default

        return answer

    raise MaxTriesReachedException(f'Valid input could not be provided after {max_invalid_count} tries.')


def not_empy_validation():
    return lambda x: x != ""


def in_list_validation(possible_values: list):
    return lambda x: x in possible_values


def yes_with_question(question: str, default=False) -> bool:
    print(f'{question} [y/n, default:{"y" if default else "n"}]')
    return yes(default)


def yes(default=False) -> bool:
    while True:
        answer = input().lower()

        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            if answer == "" and default:
                return True
            print('Provide a valid answer. [y / yes / n / no]')