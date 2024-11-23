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

    # Simula una ricarica
    saldo_aggiornato = db_service.update_credits(user_id, 5)
    db_service.create_transaction(user_id, "/ricarica", 5)
    return f"💳 Hai ricaricato 5 crediti!\n Saldo attuale: {saldo_aggiornato} crediti."
