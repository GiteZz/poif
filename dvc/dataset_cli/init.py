import yaml
import requests
import os

with open("dataset_config.yaml") as f:
    dataset_config = yaml.load(f)

headers = {
    'PRIVATE-TOKEN': dataset_config['gitlab_token']
}

current_folder = os.getcwd()

def get_groups(configuration):
    group_url = "http://datasets.jhub.be/api/v4/groups"
    r = requests.get(group_url, headers=headers,)

    return r.json()

def init_git(configuration):
    os.popen("git init")

def init_dvc(configuration):
    os.popen("dvc init")

def dvc_add_remote(configuration):


# a = get_groups()
b= 5