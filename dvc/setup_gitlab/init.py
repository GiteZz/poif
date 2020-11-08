import yaml
import requests
import os

with open("dataset_config.yaml") as f:
    dataset_config = yaml.load(f)

headers = {
    'PRIVATE-TOKEN': dataset_config['gitlab_token']
}

current_folder = os.getcwd()

def get_groups():
    group_url = "http://datasets.jhub.be/api/v4/groups"
    r = requests.get(group_url, headers=headers,)

    return r.json()

def init_git():
    os.popen("git init")

a = get_groups()
b= 5