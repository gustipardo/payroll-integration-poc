from src.employees import __init__ as emp_func
from sqlalchemy import text
class DummyReq:
def __init__(self, json):
self._json = json
def get_json(self):
return self._json
def test_ingest_employee(db_engine, monkeypatch):
# patch engine
monkeypatch.setattr('src.employees.engine', db_engine)
req = DummyReq({'employees': [{'external_id':'e1', 'name':'Alice'}]})
res = emp_func.main(req)
assert res.status_code == 200
with db_engine.begin() as conn:
r = conn.execute(text('SELECT COUNT(*) FROM employees')).fetchone()
assert r[0] == 1