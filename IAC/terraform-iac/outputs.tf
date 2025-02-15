output "kubeconfig_command" {
  value = "aws eks update-kubeconfig --region eu-central-1 --name ${aws_eks_cluster.main.name}"
}

output "eks_cluster_id" {
  description = "The EKS cluster ID"
  value       = aws_eks_cluster.main.id
}

output "eks_cluster_endpoint" {
  description = "The EKS cluster endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "eks_cluster_security_group_id" {
  description = "The security group ID attached to the EKS cluster"
  value       = aws_security_group.eks.id
}



output "jenkins_agent_token" {
  value     = kubernetes_secret.jenkins_agent_token.data["token"]
  sensitive = true
}

output "cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

# Add EKS cluster certificate configuration
output "cluster_certificate" {
  value = aws_eks_cluster.main.certificate_authority[0].data
}

output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.flask.endpoint
}

output "db_name" {
  description = "RDS database name"
  value       = aws_db_instance.flask.db_name
}

