# Create a namespace for Vault
resource "kubernetes_namespace" "vault" {
  metadata {
    name = "vault"
  }
}

# Install Vault
resource "helm_release" "vault" {
  name       = "vault"
  namespace  = kubernetes_namespace.vault.metadata[0].name
  repository = "https://helm.releases.hashicorp.com"
  chart      = "vault"
  version    = "0.27.0"

  values = [
    <<-EOF
    server:
      dataStorage:
        enabled: false
        createPVC: false
        existingClaim: "vault-pvc"
        size: 10Gi            # Storage size
      standalone:
        enabled: true        # Running in standalone mode
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: vault-pvc  
          
      volumeMounts:
      - mountPath: "/vault/data"
        name: data
        config: |
          ui = true         # Enable web interface
          listener "tcp" {
            tls_disable = 1
            address = "[::]:8200"
            cluster_address = "[::]:8201"
          }
          storage "file" {
            path = "/vault/data"
          }
    EOF
  ]

    depends_on = [
    kubernetes_namespace.vault,
    aws_eks_node_group.eks_nodes,
    kubernetes_persistent_volume_claim.vault
  ]
}