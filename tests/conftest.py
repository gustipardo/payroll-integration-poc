import os
import tempfile
import pytest
from sqlalchemy import create_engine, text
@pytest.fixture(scope='session')
def db_url():
# sqlite in-memory for tests
return 'sqlite+pysqlite:///:memory:'
@pytest.fixture(scope='function')
def db_engine(db_url):
eng = create_engine(db_url, future=True)
# create minimal schema
with eng.begin() as conn:
conn.execute(text('CREATE TABLE employees (id INTEGER PRIMARY KEY
AUTOINCREMENT, external_id TEXT UNIQUE, name TEXT, role TEXT)'))
conn.execute(text('CREATE TABLE hours (id INTEGER PRIMARY KEY
AUTOINCREMENT, employee_id INTEGER, work_date DATE, hours REAL)'))
conn.execute(text('CREATE TABLE overtime_requests (id INTEGER PRIMARY KEY
AUTOINCREMENT, employee_id INTEGER, period_start DATE, period_end DATE,
calculated_hours REAL, status TEXT DEFAULT "pending", approved_at
TIMESTAMP)'))
yield eng