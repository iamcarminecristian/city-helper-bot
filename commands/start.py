from telegram import Update

def handle(update: Update):
    """Gestisce il comando /start"""
    user = update.message.from_user
    nome = user.first_name or "Utente"
    
    return (
        f'Ciao {nome}, benvenuto in CityHelper! 🌤️🚗\n\n'
        'Ecco cosa posso fare per te:\n'
        '• /meteo [città] - Ottieni previsioni meteo attuali\n'
        '• /traffico [luogo] - Controlla situazione traffico\n'
        '• /crediti - Verifica i tuoi crediti rimanenti\n\n'
        'Scegli un comando e iniziamo!'
    )