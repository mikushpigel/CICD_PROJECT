def call() {
    sh 'docker-compose down || true'
    sh 'docker system prune -a -f || true' 
}