from telegram import Update
from telegram.ext import CallbackContext

def handle(update: Update):
    """Gestisce il comando /crediti"""
    user = update.message.from_user
    
    # In un'implementazione reale, questo valore verrebbe recuperato da un database
    crediti_iniziali = 50
    crediti_utilizzati = 10
    crediti_rimanenti = crediti_iniziali - crediti_utilizzati
    
    return (
        f"🏦 Crediti per {user.first_name}:\n"
        f"• Crediti iniziali: {crediti_iniziali}\n"
        f"• Crediti utilizzati: {crediti_utilizzati}\n"
        f"• Crediti rimanenti: {crediti_rimanenti}"
    )