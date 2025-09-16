import azure.functions as func
from ..db import engine
from sqlalchemy import text
def main(req: func.HttpRequest) -> func.HttpResponse:
try:
7
body = req.get_json()
except Exception:
return func.HttpResponse('Bad request', status_code=400)
external_id = body.get('employee_external_id')
date = body.get('date')
hours = body.get('hours')
if not (external_id and date and hours is not None):
return func.HttpResponse('Missing fields', status_code=400)
with engine.begin() as conn:
# find employee id
row = conn.execute(text('SELECT id FROM employees WHERE external_id
= :ext'), {'ext': external_id}).fetchone()
if not row:
return func.HttpResponse('Employee not found', status_code=404)
employee_id = row[0]
conn.execute(text('INSERT INTO hours (employee_id, work_date, hours)
VALUES (:eid, :d, :h)'), {'eid': employee_id, 'd': date, 'h': hours})
return func.HttpResponse('OK', status_code=200)