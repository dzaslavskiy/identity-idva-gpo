"""
Db Connection for GPO
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

from . import settings

engine = create_engine(
    settings.DB_URI, connect_args={"options": f"-csearch_path={settings.SCHEMA_NAME}"}
)

if not engine.dialect.has_schema(engine, settings.SCHEMA_NAME):
    engine.execute(CreateSchema(settings.SCHEMA_NAME))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
