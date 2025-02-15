def call() {
    if (env.SKIP_STAGE != "true") {
       sh '''
    trivy fs --exit-code 1 --scanners vuln --severity CRITICAL .
    trivy config --exit-code 1 --severity CRITICAL Dockerfile
    '''
    } else {
        echo "Skipping dependency scannig"
    }
}