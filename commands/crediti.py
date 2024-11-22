from telegram import Update
from telegram.ext import CallbackContext
from utils.cosmos_client import CosmosDBService

def handle(update: Update):
    """Gestisce il comando /crediti"""
    db_service = CosmosDBService()
    user = update.message.from_user
    user_data = db_service.get_user(user.id)

    if not user_data:
        return "Non sei ancora registrato. Usa il comando /start per iniziare."

    return (
        f"🏦 Crediti per {user.first_name}:\n"
        f"• Crediti rimanenti: {user_data['crediti']}\n"
    )
