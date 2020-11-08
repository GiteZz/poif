mkdir -p ~/.datasets
ssh-keygen -t ed25519 -C "datasets gitlab" -f ~/.datasets/gitlab_key -q -N "" -y
group_id=$(curl -s -d "name=Datasets&path=datasets" -H "PRIVATE-TOKEN: root-api-key" -X POST http://datasets.jhub.be/api/v4/groups | jq .id)
user_id=$(curl -s -d "email=dev@jhub.com&name=datasets_handler&username=datasets_handler&skip_confirmation=true&force_random_password=true&reset_password=false" -H "PRIVATE-TOKEN: root-api-key" -X POST http://datasets.jhub.be/api/v4/users | jq .id)
echo $group_id
echo $user_id
curl -d "user_id=$user_id&access_level=30" -H "PRIVATE-TOKEN: root-api-key" -X POST http://datasets.jhub.be/api/v4/groups/$group_id/members
curl -s -d "title=dataset-key&key=$(cat ~/.datasets/gitlab_key.pub)" -H "PRIVATE-TOKEN: root-api-key" -X POST http://datasets.jhub.be/api/v4/users/$user_id/keys