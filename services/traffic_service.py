import requests
from typing import Dict, Optional, Any
import logging
from datetime import datetime, timedelta
import time

class TrafficService:
    def __init__(self, subscription_key, api_key):
        self.api_key = api_key
        self.subscription_key = subscription_key
        self.base_url_geocode = "https://cityhelperbot.azure-api.net/azure-maps/search/address/json"
        self.base_url_traffic = "https://cityhelperbot.azure-api.net/azure-maps/traffic/flow/segment/json"

    def get_traffic_status(self, location):
        """Ottiene lo stato del traffico per una posizione"""
        try:
            coordinates = self._get_coordinates(location)
            if not coordinates:
                return {
                    'stato': 'Posizione non trovata',
                    'tempo_percorrenza': 'N/D',
                    'velocita_media': 'N/D'
                }

            traffic_data = self._get_traffic_data(coordinates)
            return traffic_data

        except Exception as e:
            return {
                'stato': 'Errore nel recupero dati',
                'tempo_percorrenza': 'N/D',
                'velocita_media': 'N/D'
            }

    def _get_coordinates(self, location):
        """Ottiene le coordinate geografiche di una località"""
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }
        params = {
            'api-version': '1.0',
            'query': location,
            'subscription-key': self.api_key
        }

        try:
            response = requests.get(self.base_url_geocode, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                coordinates = data['results'][0]['position']
                return {'lat': coordinates['lat'], 'lon': coordinates['lon']}
            else:
                print(f"Nessun risultato trovato per {location}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Errore nel recupero coordinate: {e}")
            return None

    def _get_traffic_data(self, coordinates):
        """Recupera i dati del traffico dalle coordinate"""
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }
        params = {
            'api-version': '1.0',
            'style': 'absolute',
            'zoom': '10',
            'subscription-key': self.api_key,
            'query': f"{coordinates['lat']},{coordinates['lon']}"
        }
    
        try:
            response = requests.get(self.base_url_traffic, headers=headers, params=params)
    
            if response.status_code == 404:
                return {
                    'stato': 'Nessun dato di traffico disponibile',
                    'velocita_media': 'N/D',
                    'tempo_percorrenza': 'N/D'
                }
    
            response.raise_for_status()
    
            # Estrarre i dati reali se disponibili
            traffic_info = response.json()
    
            if traffic_info and 'flowSegmentData' in traffic_info:
                # Estrai le informazioni specifiche dal flowSegmentData
                flow_data = traffic_info['flowSegmentData']
    
                stato = "Traffico in tempo reale"
                velocita_media = flow_data.get('currentSpeed', 'N/D')           # Velocità attuale (in km/h)
                tempo_percorrenza = flow_data.get('currentTravelTime', 'N/D')   # Tempo di percorrenza attuale in secondi
    
                # Calcoliamo il tempo di percorrenza in minuti
                tempo_percorrenza_min = round(tempo_percorrenza / 60)
    
                return {
                    'stato': stato,
                    'velocita_media': velocita_media,
                    'tempo_percorrenza': tempo_percorrenza_min
                }
            else:
                return {
                    'stato': 'Dati di traffico insufficienti',
                    'velocita_media': 'N/D',
                    'tempo_percorrenza': 'N/D'
                }
    
        except requests.exceptions.RequestException as e:
            print(f"Errore nel recupero dati traffico: {e}")
            return {
                'stato': 'Errore nel recupero dati traffico',
                'rallentamenti': 'N/D',
                'tempo_percorrenza': 'N/D'
            }
