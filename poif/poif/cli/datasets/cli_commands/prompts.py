from PyInquirer import print_json, prompt

questions = [
    {
        'type': 'list',
        'name': 'first_name',
        'message': 'What\'s your first name',
        'choices': ['Gilles','Test']
    }
]

answers = prompt(questions)
print(answers)