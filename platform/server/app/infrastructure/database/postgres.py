from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Configure postgres database connection pool
engine = create_engine(settings.POSTGRES_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_pg_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
