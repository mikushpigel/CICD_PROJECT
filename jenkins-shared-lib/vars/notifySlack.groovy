def call(String status) {
    if (status == 'success') {
        slackSend(
            channel: '#succeeded-build',
            color: 'good',
            message: "Build ${env.BUILD_NUMBER} succeeded!"
        )
    } else if (status == 'failure') {
        slackSend(
            channel: '#devops-alerts',
            color: 'danger',
            message: "Build ${env.BUILD_NUMBER} failed!"
        )
    }
}