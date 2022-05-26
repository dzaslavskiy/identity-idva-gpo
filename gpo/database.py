"""
Db Connection for GPO
"""
import sqlalchemy
from sqlalchemy import orm, schema

from . import settings

engine = sqlalchemy.create_engine(
    settings.DB_URI, connect_args={"options": f"-csearch_path={settings.SCHEMA_NAME}"}
)

if not engine.dialect.has_schema(engine, settings.SCHEMA_NAME):
    engine.execute(schema.CreateSchema(settings.SCHEMA_NAME))

SessionLocal = orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)
