resource "aws_ebs_volume" "vault" {
  availability_zone = "eu-central-1a"
  size              = 10
  type              = "gp3"
  tags = {
    Name    = "vault-ebs"
    Purpose = "vault-data"
  }
}

resource "aws_iam_role_policy" "policy_for_pv" {
  name = "policy_for_pv"
  role = data.aws_iam_role.eks_node_role.id

  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = [
        "ec2:AttachVolume",
        "ec2:CreateSnapshot",
        "ec2:CreateTags",
        "ec2:CreateVolume",
        "ec2:DeleteSnapshot",
        "ec2:DeleteTags",
        "ec2:DeleteVolume",
        "ec2:DescribeInstances",
        "ec2:DescribeSnapshots",
        "ec2:DescribeTags",
        "ec2:DescribeVolumes",
        "ec2:DetachVolume"
      ],
      Resource = "*"
    }]
  })
}

resource "helm_release" "aws_ebs_csi_driver" {
  name       = "aws-ebs-csi-driver"
  repository = "https://kubernetes-sigs.github.io/aws-ebs-csi-driver"
  chart      = "aws-ebs-csi-driver"
  namespace  = "kube-system"

  set {
    name  = "controller.serviceAccount.create"
    value = "true"
  }

  depends_on = [data.aws_eks_node_group.eks_nodes]
}

resource "kubernetes_storage_class" "ebs_sc" {
  metadata {
    name = "ebs-sc"
  }
  storage_provisioner  = "ebs.csi.aws.com"
  volume_binding_mode  = "WaitForFirstConsumer"
  parameters = {
    type = "gp3"
  }
  depends_on = [helm_release.aws_ebs_csi_driver]
}

resource "kubernetes_persistent_volume" "vault" {
  metadata {
    name = "vault-pv"
    labels = {
      type = "vault-storage"
    }
  }
  spec {
    capacity = {
      storage = "10Gi"
    }
    access_modes                   = ["ReadWriteOnce"]
    persistent_volume_reclaim_policy = "Retain"
    storage_class_name             = "ebs-sc"

    persistent_volume_source {
      csi {
        driver       = "ebs.csi.aws.com"
        volume_handle = aws_ebs_volume.vault.id
        fs_type      = "ext4"
      }
    }

    node_affinity {
      required {
        node_selector_term {
          match_expressions {
            key      = "topology.kubernetes.io/zone"
            operator = "In"
            values   = [aws_ebs_volume.vault.availability_zone]
          }
        }
      }
    }
  }
  depends_on = [kubernetes_storage_class.ebs_sc]
}

resource "kubernetes_persistent_volume_claim" "vault" {
  metadata {
    name      = "vault-pvc"
    namespace = kubernetes_namespace.vault.metadata[0].name
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "10Gi"
      }
    }
    volume_name        = kubernetes_persistent_volume.vault.metadata[0].name
    storage_class_name = "ebs-sc"
    selector {
      match_labels = {
        type = "vault-storage"
      }
    }
  }
}
