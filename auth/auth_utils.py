import urllib.parse
from utils.secret_manager import SecretManager

secret_manager = SecretManager()

def generate_auth_url(user_id):
    tenant_id = secret_manager.get_secret('AZURE-TENANT-ID')
    client_id = secret_manager.get_secret('AZURE-CLIENT-ID')
    redirect_uri = "https://cityhelpercc-bot-anb6hce5bxfhe4d0.eastus-01.azurewebsites.net/api/auth/callback"
    state = f"telegram_user_{user_id}"  # Stato per identificare l'utente al ritorno
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "response_mode": "query",
        "scope": "openid profile email",
        "state": state,
    }
    return f"{auth_url}?{urllib.parse.urlencode(params)}"
