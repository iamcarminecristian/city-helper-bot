import json
import logging
import asyncio
import azure.functions as func
from telegram import Update
from commands import start, meteo, traffico, crediti, ricarica, helper
from services.weather_service import WeatherService
from services.traffic_service import TrafficService
from utils.async_telegram_client import AsyncTelegramClient
from utils.secret_manager import SecretManager
from utils.logging_utility import LoggingUtility

# Inizializza la classe LoggingUtility per la gestione del logging
logging_utility = LoggingUtility()

# Inizializza la classe SecretManager per la gestione dei secret
secret_manager = SecretManager()

# Ottieni il logger configurato
logger = logging_utility.get_logger()

# Inizializza servizi con segreti da Key Vault/env
weather_service = WeatherService(
    secret_manager.get_secret('OPENWEATHER-API-KEY')
)
traffic_service = TrafficService(
    secret_manager.get_secret('TRAFFIC-API-KEY')
)

# Configura bot token
BOT_TOKEN = secret_manager.get_secret('TELEGRAM-BOT-TOKEN')
SECRET_TOKEN = secret_manager.get_secret('TELEGRAM-SECRET-TOKEN')

app = func.FunctionApp()

@app.route(route="main", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    """Router principale per gestire gli update di Telegram"""
    return asyncio.run(handle_telegram_update(req))

async def handle_telegram_update(req: func.HttpRequest) -> func.HttpResponse:
    """Gestore asincrono degli update di Telegram"""
    try:
        # Verifica secret token
        received_secret_token = req.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if received_secret_token != SECRET_TOKEN:
            logger.warning("Secret token non valido")
            return func.HttpResponse("Unauthorized", status_code=403)

        # Parse update
        body = req.get_body().decode('utf-8')
        update_data = json.loads(body)
        logger.info(f"Dati update ricevuti: {update_data}")

        # Crea client Telegram
        async_client = AsyncTelegramClient(BOT_TOKEN)
        bot = async_client.bot

        # Crea oggetto Update
        update = Update.de_json(update_data, bot=bot)

        # Verifica messaggio
        if not update.message:
            logger.warning("Update ricevuto senza messaggio")
            return func.HttpResponse("OK", status_code=200)

        # Estrai dati
        message_text = update.message.text
        chat_id = update.message.chat.id

        # Routing comandi
        try:
            if message_text.startswith('/start'):
                response = start.handle(update)
            elif message_text.startswith('/meteo'):
                response = meteo.handle(update, weather_service)
            elif message_text.startswith('/traffico'):
                response = traffico.handle(update, traffic_service)
            elif message_text.startswith('/crediti'):
                response = crediti.handle(update)
            elif message_text.startswith('/ricarica'):
                response = ricarica.handle(update)
            elif message_text.startswith('/help'):
                response = helper.handle(update)
            else:
                response = "Comando non riconosciuto. Usa /start per vedere i comandi disponibili."
        except Exception as command_error:
            logger.error(f"Errore nell'elaborazione del comando: {command_error}")
            response = "Si è verificato un errore durante l'elaborazione del comando."

        logger.info(f"Comando ricevuto: {message_text} da chat {chat_id}")

        # Invia risposta
        async with async_client as client:
            await client.send_message(chat_id, response)

        return func.HttpResponse(response, status_code=200)

    except Exception as e:
        logger.error(f"Errore interno: {str(e)}")
        return func.HttpResponse(f"Errore interno: {str(e)}", status_code=500)