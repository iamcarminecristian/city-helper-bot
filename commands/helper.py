from telegram import Update
from telegram.ext import CallbackContext

def handle(update: Update):
    """Gestisce il comando /help"""    
    return (
        f'Ecco cosa posso fare per te:\n'
        '• /meteo [città] - Ottieni previsioni meteo attuali\n'
        '• /traffico [luogo] - Controlla situazione traffico\n'
        '• /crediti - Verifica i tuoi crediti rimanenti\n'
        '• /ricarica - Ricarica i tuoi crediti'
        '• /help - Guida ai comandi\n\n'
    )