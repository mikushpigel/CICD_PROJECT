def call() {
    withCredentials([
        string(credentialsId: 'vault-token', variable: 'VAULT_TOKEN'),
        string(credentialsId: 'cosign-password', variable: 'COSIGN_PASSWORD')
    ]) {
        sh """
            export VAULT_ADDR='http://vault.vault.svc.cluster.local:8200'
            vault login ${VAULT_TOKEN}
            vault kv get -field=private_key secret/cosign > private.key
            vault kv get -field=public_key secret/cosign > public.key
            export COSIGN_PASSWORD=${COSIGN_PASSWORD}
            cosign sign --yes --key private.key 471112876520.dkr.ecr.eu-central-1.amazonaws.com/task-manager-app:${env.VERSION}
        """
    }
}
