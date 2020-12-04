from pathlib import Path


def remove_empty_strings(string_list):
    new_list = []

    for list_item in string_list:
        if list_item != "":
            new_list.append(list_item)

    return new_list


def folder_list_to_pathlib(folder_list):
    return [Path.cwd() / folder for folder in folder_list]


def get_url(url):
    return url + ('/' if url[-1] != '/' else '')
