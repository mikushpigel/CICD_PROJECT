def call() {
    withCredentials([
        file(credentialsId: 'private_cosign', variable: 'COSIGN_KEY'),
        string(credentialsId: 'cosign_pass', variable: 'COSIGN_PASSWORD')
    ]) {
        sh """
        export COSIGN_PASSWORD=${COSIGN_PASSWORD}
        cosign sign --yes --key "${COSIGN_KEY}" 471112876520.dkr.ecr.eu-central-1.amazonaws.com/my_app:${env.IMAGE_TAG}
        """
    }
}