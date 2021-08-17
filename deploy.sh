#!/bin/bash

if [ -n "$1" ] 
then
    s3_bucket=$1
else
    echo "Using default bucket name - but you probably do not have permission to deploy using it."
    s3_bucket="hqtrivia-deployment-us-east-1"
fi  

echo "Trying to deploy using bucket [$s3_bucket]."

stack_name="hqtgameserver"
region="us-east-1"
template="./cf-template.yaml"
template_output="./cf-template.packaged.yaml"

aws cloudformation package --template $template --s3-bucket $s3_bucket --output-template $template_output --region $region
aws cloudformation deploy --template-file $template_output --stack-name $stack_name --capabilities CAPABILITY_IAM --region $region
