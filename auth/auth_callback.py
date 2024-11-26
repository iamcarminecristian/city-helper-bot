import json
import requests
import jwt
from azure.functions import HttpRequest, HttpResponse
from utils.cosmos_client import CosmosDBService
from utils.logging_utility import LoggingUtility
from utils.secret_manager import SecretManager

logging_utility = LoggingUtility()
logger = logging_utility.get_logger()
secret_manager = SecretManager()

def auth_callback(req: HttpRequest) -> HttpResponse:
    tenant_id = secret_manager.get_secret('AZURE-TENANT-ID')
    client_id = secret_manager.get_secret('AZURE-CLIENT-ID')
    client_secret = secret_manager.get_secret('AZURE-CLIENT-SECRET')
    redirect_uri = "https://cityhelpercc-bot-anb6hce5bxfhe4d0.eastus-01.azurewebsites.net/api/auth/callback"
    logger.info(f"Configurazione: Tenant ID: {tenant_id}, Client ID: {client_id}")
    logger.info(f"Redirect URI: {redirect_uri}")

    # Ottieni il codice di autorizzazione e lo stato (che contiene l'ID Telegram)
    code = req.params.get('code')
    state = req.params.get('state')

    if not code or not state:
        logger.error("Parametri mancanti: code o state non presenti")
        return HttpResponse("Errore: Parametri mancanti", status_code=400)

    # Scambia il codice per un token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email" 
    }

    try:
        logger.info(f"URL Token: {token_url}")
        
        # Log dei dati (rimuovi il secret per sicurezza)
        log_data = data.copy()
        log_data['client_secret'] = '***HIDDEN***'
        logger.info(f"Dati richiesta: {json.dumps(log_data, indent=2)}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Log dettagliato della richiesta
        logger.info("Inizio richiesta token")
        
        response = requests.post(token_url, data=data, headers=headers)

        logger.info(f"Fine richiesta token. Status Code: {response.status_code}")

        # Log dettagliato della risposta
        logger.info(f"Response Headers: {response.headers}")
        logger.info(f"Response Text: {response.text}")

        if response.status_code != 200:
            logger.error(f"Errore nella richiesta del token. Status code: {response.status_code}")
            logger.error(f"Dettagli errore: {response.text}")
            return HttpResponse(f"Errore token: {response.text}", status_code=response.status_code)

        token_data = response.json()
        
        if "id_token" not in token_data:
            logger.error("Nessun id_token nella risposta")
            return HttpResponse("Errore: id_token mancante", status_code=400)

        # Decodifica il token
        id_token = token_data["id_token"]
        user_info = jwt.decode(id_token, options={"verify_signature": False})
        
        # Recupera l'ID Telegram dallo stato
        telegram_user_id = state.split("_")[-1]

        # Registra o aggiorna l'utente nel database
        db_service = CosmosDBService()
        user_data = db_service.get_user(telegram_user_id)
        if user_data:
            user_data["is_authenticated"] = True
            db_service.update_user(telegram_user_id, user_data)
        else:
            db_service.create_user(telegram_user_id, user_info.get("preferred_username", "Unknown"))

        return HttpResponse("Autenticazione completata! Torna al bot per continuare.", status_code=200)

    except requests.RequestException as req_error:
        logger.error(f"Errore richiesta: {req_error}")
        return HttpResponse(f"Errore di richiesta: {req_error}", status_code=500)
    except Exception as e:
        logger.error(f"Errore generico: {e}")
        return HttpResponse(f"Errore generico: {e}", status_code=500)