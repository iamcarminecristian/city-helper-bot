import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from utils.cosmos_client import CosmosDBService
from auth.auth_utils import generate_auth_url

def handle(update: Update):
    user_id = update.message.from_user.id
    db_service = CosmosDBService()

    # Verifica se l'utente è già autenticato
    user = db_service.get_user(user_id)
    if user and user.get("is_authenticated", False):
        return (
            "Bentornato! Puoi usare i seguenti comandi:\n"
            "/meteo [città]\n"
            "/traffico [luogo]\n"
            "/crediti\n"
            "/help"
        )
    else:
        auth_url = generate_auth_url(user_id)
        keyboard = [
            [InlineKeyboardButton("🔐 Accedi con Microsoft", url=auth_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        return (
            "Benvenuto in CityHelper! 🌤️🚗\n\n"
            "Per utilizzare il bot, devi prima autenticarti con Azure Entra ID.",
            reply_markup
        )