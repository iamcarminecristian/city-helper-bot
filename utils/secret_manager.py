import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class SecretManager:
    def __init__(self, key_vault_name=None):
        """
        Inizializza il gestore dei segreti.
        Supporta sia sviluppo locale che ambiente Azure.
        """

        load_dotenv()

        # Per sviluppo locale, usa le variabili di ambiente
        if not key_vault_name:
            key_vault_name = os.getenv('AZURE-KEY-VAULT-NAME')

        if key_vault_name:
            # Usa Azure Key Vault in produzione/cloud
            vault_url = f"https://{key_vault_name}.vault.azure.net/"
            credential = DefaultAzureCredential()
            self.secret_client = SecretClient(vault_url=vault_url, credential=credential)
        else:
            self.secret_client = None

    def get_secret(self, secret_name, default=None):
        """
        Recupera un secret. 
        1. Prova da Key Vault
        2. Prova da variabili ambiente
        3. Usa default
        """
        try:
            # 1. Prova Key Vault
            if self.secret_client:
                secret = self.secret_client.get_secret(secret_name)
                return secret.value

            # 2. Prova variabili ambiente
            env_secret = os.getenv(secret_name)
            if env_secret:
                return env_secret

            # 3. Usa default
            return default

        except Exception as e:
            print(f"Errore nel recuperare il secret {secret_name}: {e}")
            return default