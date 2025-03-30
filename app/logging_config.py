import logging
import json
import requests
import uuid
import time
from app.config import settings
from fastapi import Response

class DatadogHTTPHandler(logging.Handler):
    def __init__(self, api_key, site="datadoghq.eu"):
        super().__init__()
        self.api_key = api_key
        self.url = f"https://http-intake.logs.{site}/api/v2/logs"
        self.headers = {
            "Content-Type": "application/json",
            "DD-API-KEY": api_key
        }

    def emit(self, record):
        try:
            log_entry = {
                "message": record.getMessage(),
                "status": record.levelname,
                "service": "my_event_tracker_api",
                "ddsource": "python",
                "host": settings.HOST if hasattr(settings, 'HOST') else "localhost",
                "env": settings.ENVIRONMENT if hasattr(settings, 'ENVIRONMENT') else "dev"
            }
            requests.post(self.url, headers=self.headers, json=[log_entry])
        except Exception as e:
            print(f"Erreur d'envoi du log à Datadog: {e}")

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, str):
            return super().format(record)
        
        log_data = json.loads(record.msg)
        if log_data.get("type") == "request":
            return f"{self.formatTime(record)} {log_data['method']} {log_data['path']}"
        elif log_data.get("type") == "response":
            return f"{self.formatTime(record)} {log_data['method']} {log_data['path']} - {log_data['status_code']} ({log_data['response_time_ms']}ms)"
        return super().format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
dd_handler = DatadogHTTPHandler(api_key=settings.DD_API_KEY)
logger.addHandler(dd_handler)

# Configuration du handler console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter('%(asctime)s %(message)s'))
logger.addHandler(console_handler)

async def log_request_middleware(request, call_next):
    correlation_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Log de la requête entrante
    request_body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            request_body = await request.json()
        except:
            request_body = None
            
    request_log = {
        "correlation_id": correlation_id,
        "type": "request",
        "path": request.url.path,
        "method": request.method,
        "payload": request_body,
        "host": request.url.hostname or "localhost",
        "env": settings.ENVIRONMENT
    }
    logger.info(json.dumps(request_log))
    
    # Exécution de la requête
    response = await call_next(request)
    
    # Capture du corps de la réponse
    response_body = None
    if response.status_code != 204:
        # Copie du corps de la réponse
        body = [chunk async for chunk in response.body_iterator]
        # Reconstruction du corps pour le logging
        try:
            response_body = json.loads(b''.join(body).decode())
        except:
            response_body = None
            
        # Création d'une nouvelle réponse
        response = Response(
            content=b''.join(body),
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    
    # Calcul du temps de réponse
    response_time = round((time.time() - start_time) * 1000)
            
    response_log = {
        "correlation_id": correlation_id,
        "type": "response",
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "payload": response_body,
        "host": request.url.hostname or "localhost",
        "response_time_ms": response_time,
        "env": settings.ENVIRONMENT
    }
    
    if response.status_code >= 500:
        logger.error(json.dumps(response_log))
    elif response.status_code >= 400:
        logger.warning(json.dumps(response_log))
    else:
        logger.info(json.dumps(response_log))
    
    return response