pipeline {
    agent {
        docker {
            alwaysPull true
            image 'agent_repo'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u 0:0 --privileged'
        }
    }
    environment {
        API_KEY = credentials("API_KEY")
        KUBECONFIG = '/home/ubuntu/config'
        SONARQUBE_ENV = 'SonarQube'
        SONAR_PROJECT_KEY = 'my-weather-app'
        SKIP_STAGE = "true"
    }
    stages { 
        
        stage('Checkout') {
            steps {
                scmSkip(deleteBuild: true, skipPattern: '.*\\[ci skip\\].*')
            }
        }

        stage('Say Hello') {
            steps {
                script {
                    sh '''
                    echo "Hello World"
                    docker -v
                    sonar-scanner --version
                    trivy version
                    docker-compose --version
                    aws --version
                    '''
                }
            }
        }
        stage('Static Code Analysis') {
            when {
                expression { env.SKIP_STAGE != "true" }
            }
            steps {
                script {
                    withSonarQubeEnv(env.SONARQUBE_ENV) {
                        sh "sonar-scanner -Dsonar.projectKey=${env.SONAR_PROJECT_KEY} -Dsonar.sources=."
                    }
                    timeout(time: 1, unit: 'MINUTES') {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to quality gate failure: ${qg.status}"
                        }
                    }
                }
            }
        }

        stage('Dependencies Scanning') {
            when {
                expression { env.SKIP_STAGE != "true" }
            }
            steps {
                script {
                    sh '''
                    trivy fs --exit-code 1 --scanners vuln --severity CRITICAL .
                    trivy config --exit-code 1 --severity CRITICAL Dockerfile.web
                    '''
                }
            }
        }

         stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }

        stage('Test') {
            when {
                expression { env.SKIP_STAGE != "true" }
            }
            steps {
                script {
                    sh 'python3 -m unittest validation_test.py'
                }
            }
        }

        stage('Update Version in README') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'USER_ACCESS_TOKEN', usernameVariable: 'GITLAB_USERNAME', passwordVariable: 'GITLAB_TOKEN')]) {
                        def currentVersion = sh(script: "grep -oP 'Pipeline:\\K[0-9]+\\.[0-9]+\\.[0-9]+' README.md", returnStdout: true).trim()
                        if (!currentVersion) {
                            error "Version not found in README.md"
                        }
                        def (major, minor, patch) = currentVersion.tokenize('.').collect { it as int }
                        patch += 1
                        def newVersion = "${major}.${minor}.${patch}"

                        env.IMAGE_TAG = newVersion
                        echo "Updated version to ${env.IMAGE_TAG}"

                        sh """
                        git config --global --add safe.directory /home/ubuntu/workspace/cicd-pipline_develop
                        git checkout ${env.BRANCH_NAME}
                        git pull http://${GITLAB_USERNAME}:${GITLAB_TOKEN}@10.0.4.134/mika/cicd_project.git develop

                        sed -i 's/${currentVersion}/${newVersion}/' README.md
                        git config user.name "Jenkins"
                        git config user.email "jenkins@example.com"
                        git add README.md
                        git commit -m "[ci skip] Update version to ${env.IMAGE_TAG}"
                        git push http://${GITLAB_USERNAME}:${GITLAB_TOKEN}@10.0.4.134/mika/cicd_project.git develop
                        git tag ${env.IMAGE_TAG}
                        git push http://${GITLAB_USERNAME}:${GITLAB_TOKEN}@10.0.4.134/mika/cicd_project.git develop ${env.IMAGE_TAG}
                        """
                    }
                }
            }
        }
        stage('Publish') {
            steps {
                withCredentials([aws(credentialsId: 'aws_access', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                    docker tag my-web-image 471112876520.dkr.ecr.eu-central-1.amazonaws.com/my_app:${env.IMAGE_TAG}
                    docker push 471112876520.dkr.ecr.eu-central-1.amazonaws.com/my_app:${env.IMAGE_TAG}
                    """
                }
            }
        }
         stage('Sign Docker Image') {
            steps {
                withCredentials([
                    file(credentialsId: 'private_cosign', variable: 'COSIGN_KEY'),
                    string(credentialsId: 'cosign_pass', variable: 'COSIGN_PASSWORD')
                ]) {
                    script {
                        sh """
                        export COSIGN_PASSWORD=${COSIGN_PASSWORD}
                        cosign sign --yes --key "${COSIGN_KEY}" 471112876520.dkr.ecr.eu-central-1.amazonaws.com/my_app:${env.IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Verify Container Image') {
            steps {
                withCredentials([file(credentialsId: 'public_cosign', variable: 'COSIGN_PUBLIC')]) {
                    script {
                        sh """
                        cosign verify \
                        --key ${COSIGN_PUBLIC} \
                        --allow-insecure-registry \
                        --insecure-ignore-tlog=true \
                        471112876520.dkr.ecr.eu-central-1.amazonaws.com/my_app:${env.IMAGE_TAG}
                        """
                    }
                }
            }
        }

    
        // stage('Deploy to EKS') {
        //     steps {
        //         script {
        //             sh '''
        //             kubectl apply -f deployment.yml
        //             kubectl rollout status deployment/my-app-deployment
        //             kubectl get pods
        //             '''
        //         }
        //     }
        // }
    }
    post { 
        always{
                script {
                    sh 'docker-compose down || true'
                    sh 'docker system prune -a -f || true' 
                    cleanWs()
                }
        }
        success {
            slackSend (
                channel: '#succeeded-build',
                color: 'good',
                message: "Build ${env.BUILD_NUMBER} succeeded!"
            )
        }

        failure {
            slackSend (
                channel: '#devops-alerts',
                color: 'danger',
                message: "Build ${env.BUILD_NUMBER} failed!"
            )
        }
    }      

}
