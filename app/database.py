# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Load local .env if present (safe for local dev)
load_dotenv()

# Try a single DATABASE_URL first (you can put this in .env if you want)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # prefer DB_* (app local .env), else fallback to Railway-provided MYSQL* names
    DB_USER = os.getenv("DB_USER") or os.getenv("MYSQLUSER")
    DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD")
    DB_HOST = os.getenv("DB_HOST") or os.getenv("MYSQLHOST")
    DB_PORT = os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or "3306"
    DB_NAME = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE")

    if all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        DATABASE_URL = None
        logging.warning("Database env not fully configured. App will start without DB connection.")

# Expose engine/session only if DATABASE_URL is set
engine = None
SessionLocal = None
Base = declarative_base()

if DATABASE_URL:
    # pool_pre_ping avoids stale connection errors
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logging.info("Database engine created.")
else:
    logging.warning("DATABASE_URL is None: database engine was NOT created.")

# Dependency
def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database not configured. Check DB env variables.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
