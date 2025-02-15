def call() {
    withCredentials([file(credentialsId: 'public_cosign', variable: 'COSIGN_PUBLIC')]) {
        sh """
        cosign verify \
        --key ${COSIGN_PUBLIC} \
        --allow-insecure-registry \
        --insecure-ignore-tlog=true \
        471112876520.dkr.ecr.eu-central-1.amazonaws.com/my_app:${env.IMAGE_TAG}
        """
    }
}