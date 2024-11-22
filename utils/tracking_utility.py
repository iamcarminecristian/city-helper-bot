from functools import wraps
import time
from typing import Callable
import azure.functions as func
import logging

def track_function_execution(logging_utility):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            function_name = func.__name__

            try:
                # Inizia il tracciamento
                logging_utility.track_request(
                    name=f"function_start_{function_name}",
                    duration=0,
                    success=True,
                    properties={"function": function_name}
                )

                # Esegui la funzione
                result = await func(*args, **kwargs)

                # Calcola durata e traccia il successo
                duration = (time.time() - start_time) * 1000
                logging_utility.track_request(
                    name=f"function_complete_{function_name}",
                    duration=duration,
                    success=True,
                    response_code=result.status_code if hasattr(result, 'status_code') else 200
                )

                return result

            except Exception as e:
                # Traccia l'errore
                duration = (time.time() - start_time) * 1000
                logging_utility.track_request(
                    name=f"function_error_{function_name}",
                    duration=duration,
                    success=False,
                    response_code=500,
                    properties={"error": str(e)}
                )
                raise

        return wrapper
    return decorator
