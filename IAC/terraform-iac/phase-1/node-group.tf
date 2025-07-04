resource "aws_iam_role" "eks_node_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement : [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "ec2.amazonaws.com" },
    }]
  })

  tags = {
    Name = "eks-node-role"
  }
}

resource "aws_iam_role_policy_attachment" "eks_node_policies" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  ])
  role       = aws_iam_role.eks_node_role.name
  policy_arn = each.value
}


resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "eks-cluster-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  instance_types = ["t3.medium"]
  ami_type       = "AL2_x86_64"

  tags = {
    Name = "eks-cluster-node-group"
  }
}

resource "aws_iam_role_policy" "ecr_access" {
  name = "ecr-full-access"
  role = aws_iam_role.eks_node_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:*"                       
        ]
        Resource = "*"
      }
    ]
  })
}
