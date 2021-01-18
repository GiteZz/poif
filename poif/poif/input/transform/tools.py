import re
from typing import Dict


def is_template_part(part: str):
    return re.match('\{\{[^\/]*\}\}', part)


def get_template_str(part: str):
    return part.replace('{', '').replace('}', '').replace(' ', '')


def template_to_regex(template: str):
    new_template = template.replace('.', '[.]').replace('*', '.*')
    new_template, groupes = replace_template_with_regex_group(new_template)
    return new_template, groupes


def replace_template_with_regex_group(template: str):
    groups = []
    group_indices = []
    start_index = None
    for index in range(len(template) - 1):

        if template[index] == '{' and template[index + 1] == '{':
            start_index = index
        if template[index] == '}' and template[index + 1] == '}':
            stop_index = index + 2
            group_name = get_template_str(template[start_index: stop_index])
            groups.append(group_name)
            group_indices.append((start_index, stop_index))
            start_index = None

    new_template = template
    for start_index, stop_index in group_indices[::-1]:
        prefix = new_template[:start_index]
        suffix = new_template[stop_index:]
        new_template = prefix + '(.*)' + suffix

    empty_count = 0
    for index, group_name in enumerate(groups):
        if group_name == '':
            groups[index] = f'_{empty_count}'
            empty_count += 1

    return new_template, groups


def is_path_match(template: str, path: str) -> bool:
    regex_template, _ = template_to_regex(template)
    return re.match(regex_template, path)


def extract_values(template: str, path: str) -> Dict[str, str]:
    if not is_path_match(template, path):
        return {}

    template, groups = template_to_regex(template)
    matches = re.match(template, path)

    if len(matches.groups()) != len(groups):
        return {}

    return {key: value for key, value in zip(groups, matches.groups())}


def catch_all_to_value(template: str):
    """
    */*.jpg -> {{1}}/{{2}}.jpg
    """
    new_template = ""
    parts = template.split('*')
    if len(parts) == 1:
        return template

    for index, part in enumerate(parts[:-1]):
        new_template += part + "{{" + str(index) + "}}"
    new_template += parts[-1]

    return new_template

