import requests

class WeatherService:
    def __init__(self, subscription_key, api_key):
        self.api_key = api_key
        self.subscription_key = subscription_key
        self.base_url = "https://cityhelperbot.azure-api.net/weather"

    def get_weather(self, city):
        """Ottiene le previsioni meteo per una città"""
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'it'
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            
            # Verifica esplicita del codice 404 prima di raise_for_status
            if response.status_code == 404:
                raise Exception(f"Città non trovata, verifica il nome e riprova.")
            
            # Elaborazione della risposta
            data = response.json()
            
            return {
                'temperatura': round(data['main']['temp'], 1),
                'descrizione': data['weather'][0]['description'].capitalize(),
                'umidita': data['main']['humidity'],
                'vento': round(data['wind']['speed'] * 3.6, 1)  # Convert m/s to km/h
            }
        
        except requests.RequestException as e:
            # Gestione di altri errori come timeout, problemi di connessione, ecc.
            raise Exception(f"Errore nel recupero meteo: {str(e)}")
        except Exception as e:
            # Gestisce l'errore 404 e altri errori personalizzati
            raise Exception(f"{str(e)}")
