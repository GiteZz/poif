def get_existing_credentials():
    git_credential_file = '~/.git-credentials'

    existing_credentials = []

    with open(git_credential_file, 'r') as f:
        cred_line = f.readline()
        url = cred_line.split('@')[1]

        existing_credentials.append(url)

    return existing_credentials

def add_git_credential(username, password, url):
    git_credential_file = '~/.git-credentials'

    url_without_http = url.split('/')[-1]
    url_http_part = url.split(':')[0]

    new_line = f'{url_http_part}://{username}:{password}@{url_without_http}'

    with open(git_credential_file, 'a') as f:
        f.write(new_line)