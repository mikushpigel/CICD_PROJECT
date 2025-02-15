def call() {
        sh '''
             docker --version
             docker-compose --version
             docker info | grep "Server Version"
             sonar-scanner --version
             trivy version
             aws --version
         '''
        }