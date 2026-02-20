from fastapi import APIRouter
from app.services.metrics_service import MetricsService

router = APIRouter()
metrics_service = MetricsService()


@router.get("/metrics/summary")
def get_summary():
    return metrics_service.get_summary()
