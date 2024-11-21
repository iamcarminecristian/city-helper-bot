from telegram import Update
from services.weather_service import WeatherService

def handle(update: Update, weather_service: WeatherService):
    """Gestisce il comando /meteo"""
    # Estrai gli argomenti del comando
    args = update.message.text.split(' ')[1:]
    if not args:
        return 'Per favore specifica una città. Esempio: /meteo Roma'

    # Unisci gli argomenti in un'unica città
    citta = ' '.join(args)
    
    try:
        # Ottieni le previsioni meteo
        previsioni = weather_service.get_weather(citta)
        
        return (
            f"🌡️ Meteo per {citta.capitalize()}:\n"
            f"Temperatura attuale: {previsioni['temperatura']}°C\n"
            f"Condizioni: {previsioni['descrizione']}\n"
            f"Umidità: {previsioni['umidita']}%\n"
            f"Vento: {previsioni['vento']} km/h"
        )
    except Exception as e:
        return f"Impossibile recuperare le previsioni per {citta}: {str(e)}"