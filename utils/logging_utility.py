# utils/logging_utility.py
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.azure.metrics_exporter import MetricsExporter
from utils.secret_manager import SecretManager


class LoggingUtility:
    def __init__(self):
        # Inizializza il gestore dei segreti
        self.secret_manager = SecretManager()

        # Recupera la chiave di strumentazione da Azure Key Vault
        self.instrumentation_key = self.secret_manager.get_secret('INSTRUMENTATION-KEY')

        # Configura il logging e il tracciamento
        self.configure_logging()
        self.configure_tracing()
        self.configure_metrics()

    def configure_logging(self):
        """Configura il logging per l'applicazione."""
        # Crea un logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Configura il formato dei log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Gestore per la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Gestore per Azure Application Insights
        azure_handler = AzureLogHandler(
            connection_string=f"InstrumentationKey={self.instrumentation_key}"
        )
        azure_handler.setLevel(logging.INFO)
        azure_handler.setFormatter(formatter)

        # Aggiungi i gestori al logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(azure_handler)

    def configure_tracing(self):
        """Configura il tracing per Application Insights."""
        exporter = AzureExporter(
            connection_string=f"InstrumentationKey={self.instrumentation_key}"
        )
        self.tracer = Tracer(exporter=exporter, sampler=AlwaysOnSampler())

    def configure_metrics(self):
        """Configura l'esportatore di metriche per Azure Monitor."""
        self.metrics_exporter = MetricsExporter(
            connection_string=f"InstrumentationKey={self.instrumentation_key}"
        )

    def track_request(self, name: str, duration: float, success: bool,
                      response_code: int = 200, properties: dict = None):
        """Traccia una richiesta in Application Insights."""
        properties = properties or {}

        with self.tracer.span(name=name) as span:
            span.add_attribute("duration_ms", duration)
            span.add_attribute("success", success)
            span.add_attribute("response_code", response_code)
            for key, value in properties.items():
                span.add_attribute(key, value)

    def track_metric(self, name: str, value: float, properties: dict = None):
        """Traccia una metrica personalizzata."""
        properties = properties or {}
        self.metrics_exporter.export_metrics([
            {
                'name': name,
                'value': value,
                'properties': properties,
            }
        ])

    def get_logger(self):
        """Restituisce il logger configurato."""
        return self.logger
