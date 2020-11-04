build-images:
    cd ./jupyterhub/images/luxury && docker build . -t localhost:5000/luxury_nb
    docker push localhost:5000/luxury_nb
    cd ./ztjk/images/secret-sync && docker build . -t localhost:5000/secret-sync
    docker push localhost:5000/secret-sync
    cd ./ztjk/images/hub && docker build . -t localhost:5000/hub
    docker push localhost:5000/hub

upgrade: build-images
    helm upgrade --install --create-namespace jupyterhub ./ztjk/jupyterhub --cleanup-on-fail --values ./ztjk/dev-config.yaml -n jhub

clear:
    kubectl delete namespace jhub

acme:
    helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
    helm repo update
    helm upgrade --install --create-namespace pebble jupyterhub/pebble --cleanup-on-fail --values ./ztjk/dev-config-pebble.yaml -n jhub

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

hard-setup-mlflow: build-mlflow-images
    kubectl delete namespace mlflow || true
    kubectl apply -f ./mlflow/kubernetes/

setup-local-path-provision:
    kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml

setup-traefik:
    # helm repo add stable https://kubernetes-charts.storage.googleapis.com/
    helm upgrade --install traefik stable/traefik --cleanup-on-fail  --values ./traefik/values.yml
    # kubectl apply -f ./traefik/traefik_ingress.yml

setup-nginx:
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.41.0/deploy/static/provider/baremetal/deploy.yaml

setup-dvc-backend:
    kubectl apply -f ./dvc/

setup-datasets-git:
    helm  upgrade --install --create-namespace --cleanup-on-fail gitlab gitlab/gitlab --set global.hosts.domain=datasets.jhub.be --set certmanager-issuer.email=gilles.ballegeer@gmail.com -n gitlab

uninstall-k3s:
    /usr/local/bin/k3s-uninstall.sh

install-k3s:
    curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode=644  --disable-network-policy --docker

install-aws-cli:
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
