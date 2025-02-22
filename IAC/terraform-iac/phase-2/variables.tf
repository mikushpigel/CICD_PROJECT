variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "minimal-eks-cluster"
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
  default     = ["subnet-0633fce9d9a08968c", "subnet-0798641ccbcea1c26"]
}

variable "argocd_namespace" {
  description = "The namespace where ArgoCD will be installed"
  type        = string
  default     = "argocd"
}

variable "app_namespace" {
  description = "The namespace where your application will be deployed"
  type        = string
  default     = "my-flask-app"
}
variable "redis_namespace" {
  description = "ns"
  type        = string
  default     = "redis"
}

variable "git_repo_url" {
  description = "URL of the Git repository containing your application manifests"
  type        = string
  default = "http://myALB-995549484.eu-central-1.elb.amazonaws.com/mika/IAC.git"
}