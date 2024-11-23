from telegram import Update
from utils.cosmos_client import CosmosDBService
from services.weather_service import WeatherService

db_service = CosmosDBService()

def handle(update: Update, weather_service: WeatherService):
    """Gestisce il comando /meteo"""
    user = update.message.from_user
    user_id = user.id

    # Controlla i crediti
    user_data = db_service.get_user(user.id)
    if user_data['crediti'] <= 0:
        return "⚠️ Non hai crediti sufficienti per utilizzare questo comando.\n Usa /ricarica per ottenere più crediti."

    # Estrai gli argomenti
    args = update.message.text.split(' ')[1:]
    if not args:
        return 'Per favore specifica una città. Esempio: /meteo Roma'

    citta = ' '.join(args)

    try:
        previsioni = weather_service.get_weather(citta)

        # Sottrai 1 credito e salva la transazione
        db_service.delete_credits(user_id, 1)
        db_service.create_transaction(user_id, "/traffico", -1)

        return (
            f"🌡️ Meteo per {citta.capitalize()}:\n"
            f"Temperatura attuale: {previsioni['temperatura']}°C\n"
            f"Condizioni: {previsioni['descrizione']}\n"
            f"Umidità: {previsioni['umidita']}%\n"
            f"Vento: {previsioni['vento']} km/h"
        )
    except Exception as e:
        return f"Errore: {str(e)}"
