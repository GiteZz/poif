from poif.tests.integration.docker import docker_run
from poif.tests.integration.gitlab.config import GitlabConfig
from poif.tests.integration.gitlab.tools import add_git_credential
from poif.tests.integration.gitlab.wait import wait_on_url


def gitlab_setup(config: GitlabConfig):

    docker_run(config.get_docker_config())

    wait_on_url(config.get_docker_config().readiness_url)

    add_git_credential(username=config.user, password=config.password, url=config.url)