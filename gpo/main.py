"""
GPO Microservice FastAPI Web App.
"""
import logging

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from . import models, settings
from .api import router
from .database import engine

logging.basicConfig(level=settings.LOG_LEVEL)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

app.include_router(router)
