from telegram import Update
from utils.cosmos_client import CosmosDBService

db_service = CosmosDBService()

def handle(update: Update):
    """Gestisce il comando /ricarica"""
    user = update.message.from_user
    user_id = user.id

    user_data = db_service.get_user(user.id)
    if not user_data:
        return "Non sei ancora registrato. Usa il comando /start per iniziare."

    # Simula una ricarica (aggiunge 20 crediti)
    db_service.update_credits(user_id, 20)
    return f"💳 Hai ricaricato 20 crediti!\n Saldo attuale: {credit_manager.get_credits(user_id)} crediti."
