from src.overtime import __init__ as ov_func
from sqlalchemy import text
class DummyReq:
def __init__(self, json):
self._json = json
def get_json(self):
return self._json
def test_overtime_calc(db_engine, monkeypatch):
monkeypatch.setattr('src.overtime.engine', db_engine)
# seed data
with db_engine.begin() as conn:
conn.execute(text("INSERT INTO employees (external_id,name) VALUES
('e1','Alice')"))
conn.execute(text("INSERT INTO hours (employee_id, work_date, hours)
VALUES (1, '2025-08-01', 45)"))
req = DummyReq({'period_start':'2025-08-01', 'period_end':'2025-08-07'})
res = ov_func.main(req)
assert res.status_code == 200
assert 'overtime' in res.get_body().decode()