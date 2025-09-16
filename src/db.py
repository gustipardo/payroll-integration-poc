from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://
postgres:postgres@localhost:5432/payroll')
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
metadata = MetaData()
# convenience for functions
def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()