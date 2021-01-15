setup-test-environment:
    python ./poif/poif/tests/gitlab/setup.py
    python ./poif/poif/tests/minio/setup.py

setup-test-minio:
    python ./poif/poif/tests/integration/minio/setup.py

get-repo:
    python ./poif/poif/tests/gitlab/get_repo.py

sort:
    cd poif && isort .

# K3S commands

uninstall-k3s:
    /usr/local/bin/k3s-uninstall.sh

install-k3s:
    curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode=644  --disable-network-policy --docker

install-aws-cli:
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
