def call() {
    sh "cosign verify --key public.key 471112876520.dkr.ecr.eu-central-1.amazonaws.com/task-manager-app:${env.VERSION}"
}