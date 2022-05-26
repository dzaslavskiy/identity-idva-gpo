"""
GPO Microservice FastAPI Web App.
"""
import logging

import fastapi
import starlette_prometheus

from . import api, database, models, settings

logging.basicConfig(level=settings.LOG_LEVEL)

models.Base.metadata.create_all(bind=database.engine)

app = fastapi.FastAPI()

app.add_middleware(starlette_prometheus.PrometheusMiddleware)
app.add_route("/metrics/", starlette_prometheus.metrics)

app.include_router(api.router)
