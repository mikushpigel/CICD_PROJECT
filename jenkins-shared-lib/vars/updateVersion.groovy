def call(){
    withCredentials([usernamePassword(credentialsId: 'gitlab-token', usernameVariable: 'GITLAB_USERNAME', passwordVariable: 'GITLAB_TOKEN')]) {
     sh """
     git config --global --add safe.directory /home/jenkins/agent/workspace/cicd-pipline_develop
     git checkout develop
     git remote set-url origin http://$GITLAB_USERNAME:$GITLAB_TOKEN@10.0.4.134/mika/cicd_project.git 
     git remote -v
     git fetch --tags
     python3 -m semantic_release version
     python3 -m semantic_release publish
     """
    }
}