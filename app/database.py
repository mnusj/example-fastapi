from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# 1. Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base class in SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

# 4. Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()