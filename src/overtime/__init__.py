import azure.functions as func
from ..db import engine
from sqlalchemy import text
from datetime import datetime
import json
# calculates overtime for each employee between period_start and period_end
# simple rule: hours > 40 per week -> overtime = hours - 40 aggregated across
period
def main(req: func.HttpRequest) -> func.HttpResponse:
try:
body = req.get_json()
except Exception:
return func.HttpResponse('Bad request', status_code=400)
period_start = body.get('period_start')
period_end = body.get('period_end')
if not (period_start and period_end):
return func.HttpResponse('Missing period', status_code=400)
with engine.begin() as conn:
# aggregate hours per employee in period
q = text('''
8
 SELECT e.id as employee_id, e.external_id, e.name, SUM(h.hours)
as total_hours
 FROM employees e
 JOIN hours h ON h.employee_id = e.id
 WHERE h.work_date BETWEEN :s AND :e
 GROUP BY e.id, e.external_id, e.name
 ''')
rows = conn.execute(q, {'s': period_start, 'e':
period_end}).fetchall()
results = []
for r in rows:
total = float(r.total_hours)
overtime = max(0.0, total - 40.0)
# create overtime request row (pending approval)
conn.execute(text('''INSERT INTO overtime_requests (employee_id,
period_start, period_end, calculated_hours, status) VALUES
(:eid,:s,:e,:oh,'pending')'''),
{'eid': r.employee_id, 's': period_start, 'e':
period_end, 'oh': overtime})
results.append({'employee_external_id': r.external_id, 'name':
r.name, 'total_hours': total, 'overtime': overtime})
return func.HttpResponse(json.dumps({'results': results}),
status_code=200, mimetype='application/json')