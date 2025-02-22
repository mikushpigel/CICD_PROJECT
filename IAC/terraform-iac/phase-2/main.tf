terraform {
  required_providers {
    time = {
      source  = "hashicorp/time"
      version = "~> 0.9.0"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.87.0"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.35.1"
    }
    helm = {
      source = "hashicorp/helm"
      version = "2.17.0"
    }
    argocd = {
      source = "argoproj-labs/argocd"
      version = "7.3.1"
    }
  }
}

data "aws_eks_cluster" "main" {
  name = var.cluster_name
}

# Get the node group details first
data "aws_eks_node_group" "eks_nodes" {
  cluster_name    = data.aws_eks_cluster.main.name 
  node_group_name = "eks-cluster-node-group"
}

# Then reference the role ARN from the node group
data "aws_iam_role" "eks_node_role" {
  name = element(split("/", data.aws_eks_node_group.eks_nodes.node_role_arn), 1)
}