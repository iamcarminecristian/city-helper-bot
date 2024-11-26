import json
import logging
import asyncio
import azure.functions as func
from telegram import Update, ReplyKeyboardRemove
from commands import start, meteo, traffico, crediti, ricarica, helper
from services.weather_service import WeatherService
from services.traffic_service import TrafficService
from utils.async_telegram_client import AsyncTelegramClient
from utils.secret_manager import SecretManager
from utils.logging_utility import LoggingUtility
from utils.tracking_utility import track_function_execution
from utils.cosmos_client import CosmosDBService
from auth.auth_callback import auth_callback

# Inizializzazioni standard
logging_utility = LoggingUtility()
secret_manager = SecretManager()
logger = logging_utility.get_logger()

# Inizializza servizi
weather_service = WeatherService(
    secret_manager.get_secret('SUBSCRIPTION-API-KEY'),
    secret_manager.get_secret('OPENWEATHER-API-KEY')
)
traffic_service = TrafficService(
    secret_manager.get_secret('SUBSCRIPTION-API-KEY'),
    secret_manager.get_secret('TRAFFIC-API-KEY')
)

# Configura token
BOT_TOKEN = secret_manager.get_secret('TELEGRAM-BOT-TOKEN')
SECRET_TOKEN = secret_manager.get_secret('TELEGRAM-SECRET-TOKEN')

app = func.FunctionApp()

app.route(route="auth/callback", auth_level=func.AuthLevel.ANONYMOUS)(auth_callback)

@app.route(route="main", auth_level=func.AuthLevel.ANONYMOUS)
@track_function_execution(logging_utility)
async def city_helper_bot_main(req: func.HttpRequest) -> func.HttpResponse:
    """Gestore asincrono degli update di Telegram con gestione migliorata"""
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
        message_text = update.message.text.lower()
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id

        # Verifica stato di autenticazione
        db_service = CosmosDBService()
        user = db_service.get_user(user_id)
        is_authenticated = user and user.get("is_authenticated", False)

        async with async_client as client:
            # Gestione specifica per /start
            if message_text == '/start':
                if not is_authenticated:
                    # Primo utilizzo: mostra link di autenticazione
                    start_response, reply_markup = start.handle(update)
                    await client.send_message(chat_id, start_response, reply_markup=reply_markup)
                else:
                    # Utente già autenticato: mostra messaggio di benvenuto
                    await client.send_message(
                        chat_id, 
                        "Bentornato! Sei già autenticato. Usa /help per vedere i comandi disponibili.",
                        reply_markup=ReplyKeyboardRemove()
                    )
                return func.HttpResponse("OK", status_code=200)

            # Controllo autenticazione per altri comandi
            if not is_authenticated:
                await client.send_message(
                    chat_id, 
                    "⚠ Devi prima autenticarti. Usa /start per ottenere il link di autenticazione.",
                    reply_markup=ReplyKeyboardRemove()
                )
                # Rimuovi l'update corrente per evitare di bloccare la coda
                return func.HttpResponse("Unauthorized", status_code=200)

            # Routing comandi per utenti autenticati
            try:
                if message_text.startswith('/meteo'):
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
                    response = "Comando non riconosciuto. Usa /help per vedere i comandi disponibili."
            except Exception as command_error:
                logger.error(f"Errore nell'elaborazione del comando: {command_error}")
                await client.send_message(chat_id, "Si è verificato un errore durante l'elaborazione del comando.")
                return func.HttpResponse("Error", status_code=200)
            
            # Invia risposta
            await client.send_message(chat_id, response)
            
        return func.HttpResponse("OK", status_code=200)
    except Exception as e:
        logger.error(f"Errore interno: {str(e)}")
        return func.HttpResponse(f"Errore interno: {str(e)}", status_code=200)