import logging
from utils.secret_manager import SecretManager
from opencensus.ext.azure.log_exporter import AzureLogHandler

class LoggingUtility:
    def __init__(self):
        # Inizializza il gestore dei segreti
        self.secret_manager = SecretManager()

        # Recupera la chiave di strumentazione da Azure Key Vault
        self.instrumentation_key = self.secret_manager.get_secret('INSTRUMENTATION-KEY')

        # Configura il logging
        self.configure_logging()

    def configure_logging(self):
        """Configura il logging per l'applicazione."""
        # Crea un logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Aggiungi il gestore per Azure Application Insights
        azure_handler = AzureLogHandler(connection_string=f"InstrumentationKey={self.instrumentation_key}")
        logger.addHandler(azure_handler)

        # Aggiungi anche il logging di base nella console
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logger = logger

    def get_logger(self):
        """Restituisce il logger configurato."""
        return self.logger
