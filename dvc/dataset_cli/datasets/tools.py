def yes():
    while True:
        answer = input().lower()

        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print('Provide a valid answer. [y / yes / n / no]')