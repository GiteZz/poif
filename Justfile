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
    helm upgrade --install --create-namespace minio minio_charts/minio --cleanup-on-fail  -n minio

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
