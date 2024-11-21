import logging
import asyncio
import aiohttp
from telegram import Bot

logger = logging.getLogger(__name__)

class AsyncTelegramClient:
    """Client asincrono per inviare messaggi Telegram"""
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.session = None
        self.bot = Bot(token=bot_token)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def send_message(self, chat_id: int, text: str, max_retries: int = 3):
        """Invia un messaggio Telegram con gestione dei tentativi"""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }

        for attempt in range(max_retries):
            try:
                async with self.session.post(url, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"Messaggio inviato a chat {chat_id}")
                        return True
                    else:
                        logger.warning(f"Errore {response.status} nell'invio del messaggio. Tentativo {attempt + 1}")
            except Exception as e:
                logger.error(f"Eccezione durante l'invio: {e}. Tentativo {attempt + 1}")
                await asyncio.sleep(1)  # Breve pausa tra i tentativi

        logger.error(f"Invio messaggio fallito dopo {max_retries} tentativi")
        return False