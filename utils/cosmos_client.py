import os
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions, PartitionKey
from utils.secret_manager import SecretManager

# Inizializza la classe SecretManager per la gestione dei secret
secret_manager = SecretManager()

class CosmosDBService:
    def __init__(self):
        url = secret_manager.get_secret('COSMOS-DB-URL')
        key = secret_manager.get_secret('COSMOS-DB-KEY')
        database_name = "cityhelperccbot-db"
        container_name = "users"

        # Inizializza il client
        self.client = CosmosClient(url, credential=key)
        self.database = self.client.create_database_if_not_exists(database_name)
        self.container = self.database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/userId"),
            offer_throughput=400
        )

    def create_user(self, user_id, username):
        """Crea un nuovo documento per l'utente"""
        try:
            self.container.create_item({
                "id": str(user_id),
                "userId": str(user_id),
                "username": username,
                "crediti": 50,
                "createdAt": datetime.utcnow().isoformat(),
                "updatedAt": datetime.utcnow().isoformat()
            })
        except exceptions.CosmosResourceExistsError:
            pass  # Utente già esistente

    def get_user(self, user_id):
        """Recupera i crediti di un utente"""
        try:
            return self.container.read_item(item=str(user_id), partition_key=str(user_id))
        except exceptions.CosmosResourceNotFoundError:
            return None

    def update_credits(self, user_id, qty):
        """Aggiorna i crediti di un utente"""
        user = self.get_user(user_id)
        if user:
            user["crediti"] += qty
            user["updatedAt"] = datetime.utcnow().isoformat()
            self.container.upsert_item(user)

    def delete_credits(self, user_id, qty):
        """Deduce un credito quando un comando viene utilizzato"""
        user = self.get_user(user_id)
        if user:
            user["crediti"] -= qty
            user["updatedAt"] = datetime.utcnow().isoformat()
            self.container.upsert_item(user)