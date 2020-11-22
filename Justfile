# Setup DVC and components

setup-datasets-namespace:
    kubectl apply -f ./dvc/namespace.yml

clear-datasets-namespace:
    -kubectl delete namespace dvc # This line is allowed to fail because the namespace could've already been deleted

setup-datasets-gitlab:
    kubectl apply -f ./dvc/gitlab/

setup-datasets-minio:
    kubectl apply -f ./dvc/minio/

setup-dvc: setup-datasets-namespace setup-datasets-gitlab setup-datasets-minio

hard-setup-dvc: clear-datasets-namespace setup-dvc
    kubectl rollout status deployment dvc-gitlab-deployment -n dvc
    kubectl exec -it $(kubectl get pods -n dvc -l=app=dvc-gitlab -o name) -n dvc -- gitlab-rails runner "token = User.find_by_username('root').personal_access_tokens.create(scopes: [:api], name: 'Automation token');token.set_token('root-api-key');token.save!"
    ./dvc/gitlab/set_dataset_configuration.sh
    kubectl rollout status deployment dvc-minio-backend -n dvc
    ./dvc/minio/apply_bucket_policy.sh

build-hub-images:
    cd ./jupyter/images/luxury && docker build . -t localhost:5000/luxury_nb
    docker push localhost:5000/luxury_nb
    cd ./ztjk/images/secret-sync && docker build . -t localhost:5000/secret-sync
    docker push localhost:5000/secret-sync
    cd ./ztjk/images/hub && docker build . -t localhost:5000/hub
    docker push localhost:5000/hub

setup-acme:
    helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
    helm repo update
    helm upgrade --install --create-namespace pebble jupyterhub/pebble --cleanup-on-fail --values ./ztjk/dev-config-pebble.yaml -n jhub

setup-hub: build-hub-images setup-acme
    helm upgrade --install --create-namespace jupyterhub ./ztjk/jupyterhub --cleanup-on-fail --values ./ztjk/dev-config.yaml -n jhub

clear-hub:
    kubectl delete namespace jhub

remove-acme:
    kubectl delete deployment.apps pebble-coredns -n default
    kubectl delete deployment.apps pebble -n default
    kubectl delete svc pebble-coredns -n default
    kubectl delete svc pebble -n default

easy-commands:
    source $(alias kall="kubectl get all -n jub")

setup-docker-registry:
    docker run -d -p 5000:5000 --restart=always --name registry registry:2

setup-minio:
    kubectl delete namespace minio
    helm upgrade --install --create-namespace minio minio_charts/minio --cleanup-on-fail  -n minio
    kubectl apply -f ./config/kubernetes/ugent_ingress.yml

setup-alluxio:
    helm repo add alluxio-charts https://alluxio-charts.storage.googleapis.com/openSource/2.4.0
    helm upgrade --install --create-namespace alluxio alluxio-charts/alluxio --cleanup-on-fail --values ./config/alluxio_helm_config.yml -n alluxio
    kubectl apply -f ./config/kubernetes/alluxio_ui_forward.yml

build-mlflow-images:
    cd ./mlflow/docker_images/mlflow_server && docker build . -t localhost:5000/mlflow_server
    docker push localhost:5000/mlflow_server

clear-mlflow:
    kubectl delete namespace mlflow || true

setup-mlflow: build-mlflow-images clear-mlflow
    kubectl apply -f ./mlflow/kubernetes/


build-jupyter-test:
    cd ./jupyter/images/extension_test && docker build . -t localhost:5000/extension_test
    docker push localhost:5000/extension_test

setup-jupyter-docker: build-jupyter-test
    -docker stop test_jupyter
    -docker rm test_jupyter
    docker run -d -p 8888:8888 -e JUPYTER_TOKEN=token --name test_jupyter localhost:5000/extension_test

setup-pypi:
    kubectl apply -f ./pypi/namespace.yml
    kubectl apply -f ./pypi/

# K3S commands

uninstall-k3s:
    /usr/local/bin/k3s-uninstall.sh

install-k3s:
    curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode=644  --disable-network-policy --docker

install-aws-cli:
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
