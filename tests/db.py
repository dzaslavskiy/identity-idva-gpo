import sqlalchemy
from sqlalchemy import orm, pool

engine = sqlalchemy.create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=pool.StaticPool,
)

SessionLocal = orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)
