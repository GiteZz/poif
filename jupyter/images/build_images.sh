cd "$(dirname "$0")"

cd luxury
docker build . -t localhost:5000/luxury_nb
docker push localhost:5000/luxury_nb