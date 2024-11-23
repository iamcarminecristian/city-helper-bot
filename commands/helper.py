from telegram import Update
from telegram.ext import CallbackContext

def handle(update: Update):
    """Gestisce il comando /help"""    
    return (
        f'Ecco cosa posso fare per te:\n'
        '/meteo [città] - Previsioni meteo\n'
        '/traffico [luogo] - Situazione traffico\n'
        '/crediti - Verifica i tuoi crediti\n'
        '/ricarica - Ricarica i tuoi crediti\n'
        '/help - Guida ai comandi\n\n'
    )