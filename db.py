from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 👇 get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5434/fast")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 👇 create all tables
def create_table():
    Base.metadata.create_all(bind=engine)

# 👇 FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
