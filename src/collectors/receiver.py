from fastapi import FastAPI, BackgroundTasks, HttpException
from src.core.schema import IncidentContext
import uuid
import logging


app = FastAPI(title="Aether-SRE Ingestor")


logger = logging.getLogger(__name__)


async def start_investigation(context: IncidentContext):
    logger.info(f"Starting Investigation for {context.incident_id} on {context.service_name}")
    pass


@app.post("/v1/alerts")
async def handle_alert(payload: Dict, background_tasks: BackgroundTasks):
    """
    Ingests alerts from Prometheus AlertManager for OTLP Exporters.
    """
    try:
        context = IncidentContext(
            incident_id=str(uuid.uuid4()),
            service_name=payload.get("labels", {}).get("service", "unknown"),
            severity=payload.get("labels", {}).get("severity", "unknown"),
        )
        background_tasks.add_task(start_investigation, context)
        return { "status": "accepted", "incident_id": context.incident_id }
    except Exception as e:
        raise HttpException(status_code=400, detail=str(e))