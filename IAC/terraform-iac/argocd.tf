# -- Data Sources for EKS --
data "aws_eks_cluster" "main" {
  name = aws_eks_cluster.main.name
}

# -- Helm Release for ArgoCD --
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "5.46.7"
  namespace  = kubernetes_namespace.argocd.metadata[0].name

  set {
    name  = "server.service.type"
    value = "ClusterIP"
  }

  set {
    name  = "server.extraArgs"
    value = "{--insecure}"
  }

  set {
    name  = "installCRDs"
    value = "true"
  }


  depends_on = [
    kubernetes_namespace.argocd,
    aws_eks_node_group.eks_nodes,
    aws_eks_cluster.main  
  ]
}

# -- ArgoCD Service Account --
resource "kubernetes_service_account" "argocd" {
  metadata {
    name      = "argocd-sa"
    namespace = kubernetes_namespace.argocd.metadata[0].name
  }
}

# -- ArgoCD Cluster Role --
resource "kubernetes_cluster_role" "argocd" {
  metadata {
    name = "argocd-cluster-role"
  }

  rule {
    api_groups = ["*"]
    resources  = ["*"]
    verbs      = ["*"]
  }
}

# -- ArgoCD Cluster Role Binding --
resource "kubernetes_cluster_role_binding" "argocd" {
  metadata {
    name = "argocd-cluster-role-binding"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.argocd.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.argocd.metadata[0].name
    namespace = kubernetes_namespace.argocd.metadata[0].name
  }
}

data "kubernetes_service" "argocd_server" {
  metadata {
    name      = "argocd-server"
    namespace = kubernetes_namespace.argocd.metadata[0].name
  }
  depends_on = [helm_release.argocd]
}

data "kubernetes_secret" "argocd_admin_password" {
  metadata {
    name      = "argocd-initial-admin-secret"
    namespace = kubernetes_namespace.argocd.metadata[0].name
  }
  depends_on = [helm_release.argocd]
}

# -- ArgoCD Application for The App --
resource "kubernetes_manifest" "the_app" {
  
  manifest = {
    "apiVersion" = "argoproj.io/v1alpha1"
    "kind"       = "Application"
    "metadata" = {
      "name"      = "the-app"
      "namespace" = "argocd"
    }
    "spec" = {
      "project" = "default"
      "source" = {
        "repoURL"        = var.git_repo_url
        "targetRevision" = "HEAD"
        "path"           = "kubernetes/app"
      }
      "destination" = {
        "server"    = "https://kubernetes.default.svc"
        "namespace" = "my-flask-app"
      }
      "syncPolicy" = {
        "automated" = {
          "prune"    = true
          "selfHeal" = true
        }
      }
    }
  }
  depends_on = [
    helm_release.argocd
  ]
}

# -- ArgoCD Application for The Redis --
resource "kubernetes_manifest" "the-redis" {
  manifest = {
    "apiVersion" = "argoproj.io/v1alpha1"
    "kind"       = "Application"
    "metadata" = {
      "name"      = "the-redis"
      "namespace" = "argocd"
    }
    "spec" = {
      "project" = "default"
      "source" = {
        "repoURL"        = var.git_repo_url
        "targetRevision" = "HEAD"
        "path"           = "kubernetes/redis"
      }
      "destination" = {
        "server"    = "https://kubernetes.default.svc"
        "namespace" = "redis"
      }
      "syncPolicy" = {
        "automated" = {
          "prune"    = true
          "selfHeal" = true
        }
      }
    }
  }
  depends_on = [
    helm_release.argocd
  ]
}

output "argocd_admin_password" {
  description = "ArgoCD Admin Password"
  value       = nonsensitive(data.kubernetes_secret.argocd_admin_password.data["password"])
  sensitive   = true
}

output "argocd_url" {
  description = "ArgoCD ClusterIP Service URL"
  value       = "http://${data.kubernetes_service.argocd_server.spec.0.cluster_ip}:80"
}
