import azure.functions as func
from ..db import engine
from sqlalchemy import text
def main(req: func.HttpRequest) -> func.HttpResponse:
# path param: id
rid = req.route_params.get('id')
if not rid:
return func.HttpResponse('Missing id', status_code=400)
body = None
try:
body = req.get_json()
except Exception:
pass
action = (body or {}).get('action','approve')
if action not in ('approve','reject'):
return func.HttpResponse('Bad action', status_code=400)
status = 'approved' if action=='approve' else 'rejected'
with engine.begin() as conn:
conn.execute(text('UPDATE overtime_requests SET status = :s,
9
approved_at = now() WHERE id = :id'), {'s': status, 'id': rid})
return func.HttpResponse('OK', status_code=200)