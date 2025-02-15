def call() {
    withCredentials([aws(credentialsId: 'aws_access', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
        sh """
        # Login to ECR
        aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 471112876520.dkr.ecr.eu-central-1.amazonaws.com
        
        # Tag and push
        docker tag task-manager-app 471112876520.dkr.ecr.eu-central-1.amazonaws.com/task-manager-app:latest
        docker push 471112876520.dkr.ecr.eu-central-1.amazonaws.com/task-manager-app:latest
        """
    }
}