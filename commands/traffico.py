from telegram import Update
from utils.cosmos_client import CosmosDBService
from services.traffic_service import TrafficService

db_service = CosmosDBService()

def handle(update: Update, traffic_service: TrafficService):
    """Gestisce il comando /traffico"""
    user = update.message.from_user
    user_id = user.id

    # Controlla i crediti
    user_data = db_service.get_user(user.id)
    if user_data['crediti'] <= 0:
        return "⚠️ Non hai crediti sufficienti per utilizzare questo comando.\n Usa /ricarica per ottenere più crediti."
    
    # Estrai gli argomenti del comando
    args = update.message.text.split(' ')[1:]
    if not args:
        return 'Per favore specifica un luogo. Esempio: /traffico Napoli'

    # Unisci gli argomenti in un unico luogo
    luogo = ' '.join(args)
    
    try:
        # Ottieni informazioni sul traffico
        info_traffico = traffic_service.get_traffic_status(luogo)
        
        # Sottrai 1 credito e salva la transazione
        db_service.delete_credits(user_id, 1)
        db_service.create_transaction(user_id, "/traffico", -1)

        if info_traffico['stato'] == 'Posizione non trovata':
            return f"⚠️ Non sono riuscito a trovare il luogo: {luogo}. Per favore, verifica che il nome sia corretto."
        
        if info_traffico['stato'] == 'Errore nel recupero dati':
            return "⚠️ Si è verificato un errore nel recupero delle informazioni sul traffico. Riprova più tardi."

        return (
            f"🚦 Situazione traffico per {luogo.capitalize()}:\n"
            f"Stato: {info_traffico['stato']}\n"
            f"Velocita media: {info_traffico['velocita_media']} km\n"
            f"Tempo di percorrenza: {info_traffico['tempo_percorrenza']} min\n"
        )
    except Exception as e:
        return f"Errore: {str(e)}"
