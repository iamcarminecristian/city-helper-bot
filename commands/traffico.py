from telegram import Update
from services.traffic_service import TrafficService

def handle(update: Update, traffic_service: TrafficService):
    """Gestisce il comando /traffico"""
    # Estrai gli argomenti del comando
    args = update.message.text.split(' ')[1:]
    if not args:
        return 'Per favore specifica un luogo. Esempio: /traffico Napoli'

    # Unisci gli argomenti in un unico luogo
    luogo = ' '.join(args)
    
    try:
        # Ottieni informazioni sul traffico
        info_traffico = traffic_service.get_traffic_status(luogo)
        
        return (
            f"🚦 Situazione traffico per {luogo.capitalize()}:\n"
            f"Stato: {info_traffico['stato']}\n"
            f"Rallentamenti: {info_traffico['rallentamenti']} km\n"
            f"Tempo stimato di percorrenza: {info_traffico['tempo_percorrenza']} min"
        )
    except Exception as e:
        return f"Impossibile recuperare info traffico per {luogo}: {str(e)}"