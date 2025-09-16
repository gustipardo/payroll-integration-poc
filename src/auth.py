import os
import jwt
from functools import wraps
from azure.functions import HttpRequest, HttpResponse
SECRET = os.getenv('JWT_SECRET', 'dev-secret')
5
class Unauthorized(Exception):
pass
def require_jwt(func):
@wraps(func)
def wrapper(req: HttpRequest, *args, **kwargs):
auth = req.headers.get('Authorization','')
if not auth.startswith('Bearer '):
return HttpResponse('Unauthorized', status_code=401)
token = auth.split(' ',1)[1]
try:
payload = jwt.decode(token, SECRET, algorithms=['HS256'])
req.route_params['user'] = payload
except Exception:
return HttpResponse('Unauthorized', status_code=401)
return func(req, *args, **kwargs)
return wrapper