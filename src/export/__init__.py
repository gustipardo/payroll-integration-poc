import azure.functions as func
from ..db import engine
from sqlalchemy import text
from ..utils import to_csv
def main(req: func.HttpRequest) -> func.HttpResponse:
with engine.begin() as conn:
rows = conn.execute(text('''
 SELECT o.id, e.external_id, e.name, o.period_start, o.period_end,
o.calculated_hours
 FROM overtime_requests o
 JOIN employees e ON e.id = o.employee_id
 WHERE o.status = 'approved'
 ''')).fetchall()
items = [
{ 'id': r.id, 'external_id': r.external_id, 'name': r.name,
'period_start': r.period_start, 'period_end': r.period_end, 'overtime':
float(r.calculated_hours or 0)}
for r in rows
]
csv_text = to_csv(items,
['id','external_id','name','period_start','period_end','overtime'])
return func.HttpResponse(csv_text, status_code=200, mimetype='text/csv')