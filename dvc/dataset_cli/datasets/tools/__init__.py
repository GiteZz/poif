def yes(empy_is_true=False):
    while True:
        answer = input().lower()

        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            if answer == "" and empy_is_true:
                return True
            print('Provide a valid answer. [y / yes / n / no]')


def remove_empty_strings(string_list):
    new_list = []

    for list_item in string_list:
        if list_item != "":
            new_list.append(list_item)

    return new_list