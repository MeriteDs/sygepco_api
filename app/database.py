from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ✅ URL de la base de données PostgreSQL (Render)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sygepco_user:6joG4be7YJf8zP810P25Tgn0Z7WJYpCD@dpg-d8vud4jeo5us73blo3d0-a.oregon-postgres.render.com:5432/sygepco_db"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()