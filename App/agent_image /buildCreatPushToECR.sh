#!/bin/bash

AWS_ACCOUNT_ID="471112876520"
AWS_REGION="eu-central-1"
ECR_REPO_NAME="my-agent-image"
IMAGE_TAG="latest"


docker build -t $ECR_REPO_NAME .

docker tag $ECR_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

aws ecr describe-repositories --repository-names $ECR_REPO_NAME --region $AWS_REGION || aws ecr create-repository --repository-name $ECR_REPO_NAME --region $AWS_REGION

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG