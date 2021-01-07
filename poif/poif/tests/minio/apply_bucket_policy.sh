cd "$(dirname "$0")"

aws --profile datasets --endpoint-url http://datasets.backend.jhub.be s3api put-bucket-policy --bucket datasets-images --policy file://./config/policy.json
