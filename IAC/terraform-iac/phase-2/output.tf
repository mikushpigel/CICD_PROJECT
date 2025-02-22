output "argocd_admin_password" {
  description = "ArgoCD Admin Password"
  value       = nonsensitive(data.kubernetes_secret.argocd_admin_password.data["password"])
  sensitive   = true
}

output "argocd_url" {
  description = "ArgoCD ClusterIP Service URL"
  value       = "http://${data.kubernetes_service.argocd_server.spec.0.cluster_ip}:80"
}

output "jenkins_agent_token" {
  value     = kubernetes_secret.jenkins_agent_token.data["token"]
  sensitive = true
}


