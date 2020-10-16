cd "$(dirname "$0")"
../jupyterhub/images/build_images.sh
cd "$(dirname "$0")"
helm upgrade --install jupyterhub ./jupyterhub --cleanup-on-fail --values dev-config.yaml