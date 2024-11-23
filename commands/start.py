from telegram import Update
from telegram.ext import CallbackContext
from utils.cosmos_client import CosmosDBService

def handle(update: Update):
    """Gestisce il comando /start"""
    user = update.message.from_user
    nome = user.first_name or "Utente"

    db_service = CosmosDBService()
    user_data = db_service.get_user(user.id)
    if not user_data:
        db_service.create_user(user.id, user.username)
    
    return (
        f'Ciao {nome}, benvenuto in CityHelper! 🌤️🚗\n\n'
        'Ecco cosa posso fare per te:\n'
        '/meteo [città] - Previsioni meteo\n'
        '/traffico [luogo] - Situazione traffico\n'
        '/crediti - Verifica i tuoi crediti\n'
        '/ricarica - Ricarica i tuoi crediti\n'
        '/help - Guida ai comandi\n\n'
        'Scegli un comando e iniziamo!'
    )