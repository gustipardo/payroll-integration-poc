import azure.functions as func
import json
from ..db import engine
from sqlalchemy import text
# simple HTTP-trigger function to ingest employees
def main(req: func.HttpRequest) -> func.HttpResponse:
try:
6
body = req.get_json()
except ValueError:
return func.HttpResponse('Bad request', status_code=400)
emps = body.get('employees', [])
if not emps:
return func.HttpResponse('No employees', status_code=400)
with engine.begin() as conn:
for e in emps:
conn.execute(text(
"INSERT INTO employees (external_id, name, role) VALUES
(:external_id, :name, :role) ON CONFLICT (external_id) DO UPDATE SET name =
EXCLUDED.name, role = EXCLUDED.role"
), { 'external_id': e['external_id'], 'name': e['name'], 'role':
e.get('role') })
return func.HttpResponse(json.dumps({'ok': True}), status_code=200,
mimetype='application/json')