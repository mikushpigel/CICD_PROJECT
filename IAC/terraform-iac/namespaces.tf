# -- ArgoCD Namespace --
resource "kubernetes_namespace" "argocd" {
  metadata {
    name = var.argocd_namespace
  }
}

resource "kubernetes_namespace" "jenkins_ns" {
  metadata {
    name = "jenkins-ns"  
}
}

resource "kubernetes_namespace" "redis" {
  metadata {
    name = var.redis_namespace  
  }
}

resource "kubernetes_namespace" "my-flask-app" {
  metadata {
    name = var.app_namespace  
  }
}
