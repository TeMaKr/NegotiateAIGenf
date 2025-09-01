from typing import Dict

import httpx
import redis
from celery import Celery
from fastapi import APIRouter, HTTPException

from settings import settings

# Create router for health check endpoints
router = APIRouter()


@router.get("/healthz")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint that verifies connectivity to PocketBase, Redis, and Celery
    Returns status of all dependent services
    """
    health_status = {
        "status": "healthy",
        "pocketbase": "unknown",
        "redis": "unknown",
        "celery": "unknown",
    }

    # Check PocketBase connectivity
    try:
        # Use the PocketBase API host from settings

        if not settings.pocketbase_api.host:
            raise ValueError("PocketBase API host is not configured.")
        pocketbase_url = settings.pocketbase_api.host
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{pocketbase_url}/api/health", timeout=5.0)
            if response.status_code == 200:
                health_status["pocketbase"] = "healthy"
            else:
                health_status["pocketbase"] = "unhealthy"
                health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["pocketbase"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Redis connectivity using application settings
    try:
        redis_client = redis.Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            decode_responses=True,
        )

        # Simple ping to test connection
        redis_client.ping()
        health_status["redis"] = "healthy"
    except Exception as e:
        health_status["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Celery worker connectivity
    try:
        # Create Celery app instance with the same broker as your main app
        broker_url = settings.redis.dsn
        celery_app = Celery("healthcheck", broker=broker_url)

        # Configure result backend
        celery_app.conf.update(
            result_backend=broker_url,
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
        )

        # Get active workers with timeout
        inspect = celery_app.control.inspect(timeout=3.0)
        active_workers = inspect.active()

        if active_workers and len(active_workers) > 0:
            # Check if any workers are responsive
            stats = inspect.stats()
            if stats and len(stats) > 0:
                health_status["celery"] = f"healthy ({len(stats)} workers)"
            else:
                health_status["celery"] = "unhealthy: workers not responding"
                health_status["status"] = "unhealthy"
        else:
            health_status["celery"] = "unhealthy: no active workers"
            health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["celery"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    # Return 503 if any service is unhealthy
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)

    return health_status
