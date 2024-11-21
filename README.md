city_helper_cc_bot/
│
├── main.py                  # Punto di ingresso (router principale)
├── commands/
│   ├── __init__.py          # Permette di trattare la directory come un modulo
│   ├── start.py             # Funzione per il comando /start
│   ├── meteo.py             # Funzione per il comando /meteo
│   ├── traffico.py          # Funzione per il comando /traffico
│   ├── crediti.py           # Funzione per il comando /crediti
│
├── requirements.txt         # Librerie necessarie (telegram, azure-functions)
└── function.json            # Configurazione per Azure Function (HTTP Trigger)
