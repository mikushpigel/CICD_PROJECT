def call() {
    if (env.SKIP_STAGE != "true") {
        withSonarQubeEnv('SonarQube') {  
                sh """
                    sonar-scanner \\
                        -Dsonar.projectKey=${env.SONAR_PROJECT_KEY} \\
                        -Dsonar.sources=.
                """
            }
    } else {
        echo "Skipping Quality Gate stage"
    }
}