import requests

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        """Ottiene le previsioni meteo per una città"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'it'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperatura': round(data['main']['temp'], 1),
                'descrizione': data['weather'][0]['description'].capitalize(),
                'umidita': data['main']['humidity'],
                'vento': round(data['wind']['speed'] * 3.6, 1)  # Convert m/s to km/h
            }
        except requests.RequestException as e:
            raise Exception(f"Errore nel recupero meteo: {str(e)}")