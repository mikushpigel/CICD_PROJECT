data "aws_ecr_authorization_token" "token" {
  registry_id = "471112876520"
}

resource "kubernetes_secret" "mysec"{
  metadata {
    name      = "mysec"
    namespace = "jenkins-ns"
  }

  type = "kubernetes.io/dockerconfigjson"

  data = {
    ".dockerconfigjson" = jsonencode({
      auths = {
        "${data.aws_ecr_authorization_token.token.proxy_endpoint}" = {
          "username" = data.aws_ecr_authorization_token.token.user_name
          "password" = data.aws_ecr_authorization_token.token.password
          "email"    = "no-reply@example.com"
          "auth"     = base64encode("${data.aws_ecr_authorization_token.token.user_name}:${data.aws_ecr_authorization_token.token.password}")
        }
      }
    })
  }

  depends_on = [
    kubernetes_namespace.jenkins_ns
  ]
}