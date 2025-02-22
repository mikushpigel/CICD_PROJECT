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

variable "vpc_id" {
 description = "ID of the VPC"
  type        = string
  default     = "vpc-06bde0222ba512891"
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
  default     = ["subnet-0633fce9d9a08968c", "subnet-0798641ccbcea1c26"]
}

variable "public_subnets" {
  description = "List of subnet IDs"
  type        = list(string)
  default     = ["subnet-0ffee7408feb0dcef", "subnet-0f11ba17b21b64434"]
}

variable "db_username" {
  description = "Username for the RDS database"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Password for the RDS database"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "task_manager_db"
}

