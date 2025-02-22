output "kubeconfig_command" {
  value = "aws eks update-kubeconfig --region eu-central-1 --name ${aws_eks_cluster.main.name}"
}

output "eks_cluster_endpoint" {
  description = "The EKS cluster endpoint"
  value       = aws_eks_cluster.main.endpoint
}



