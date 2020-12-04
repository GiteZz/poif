from poif.data_interface.tools.config import S3Config


def simple_input(title: str, value_when_empty="", use_empy_value=True) -> str:
    if value_when_empty != "" and use_empy_value:
        print(f'{title}: [default: {value_when_empty}]')
    else:
        print(f'{title}: ')

    while True:
        answer = input()
        if answer != "":
            return answer
        elif use_empy_value:
            return value_when_empty
        else:
            print('Please provide valid answer')


def yes_with_question(question: str, empty_is_true=False) -> bool:
    print(f'{question} [y/n, default:{"y" if empty_is_true else "n"}]')
    return yes(empty_is_true)


def yes(empy_is_true=False) -> bool:
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


def s3_input(default_bucket="", default_endpoint="", default_profile="") -> S3Config:
    s3_config = {}
    s3_config['bucket'] = simple_input(
        'S3 bucket',
        value_when_empty=default_bucket
    )
    s3_config['endpoint'] = simple_input(
        'S3 endpoint',
        value_when_empty=default_endpoint
    )
    s3_config['profile'] = simple_input(
        'S3 profile',
        value_when_empty=default_profile
    )

    return S3Config(**s3_config)