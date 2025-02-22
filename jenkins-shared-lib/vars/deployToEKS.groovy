def call(){
    withCredentials([usernamePassword(credentialsId: 'iac-token', usernameVariable: 'GITLAB_USERNAME', passwordVariable: 'GITLAB_TOKEN')]) {
     sh """
     git clone http://$GITLAB_USERNAME:$GITLAB_TOKEN@10.0.4.134/mika/IAC.git 
     cd IAC
     git config user.email "podagent@example.com"
     git config user.name "podAgent"
     sed -i 's|image: .*|image: 471112876520.dkr.ecr.eu-central-1.amazonaws.com/task-manager-app:${env.VERSION}|' kubernetes/app/deployment.yml
     git add kubernetes/app/deployment.yml
     git commit -m "update image version in deployment file"
     git push origin main
     """
    }
}

