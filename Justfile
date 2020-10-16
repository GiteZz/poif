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