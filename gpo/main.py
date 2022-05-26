"""
GPO Microservice FastAPI Web App.
"""
import logging

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from . import api, database, models, settings

logging.basicConfig(level=settings.LOG_LEVEL)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

app.include_router(api.router)
