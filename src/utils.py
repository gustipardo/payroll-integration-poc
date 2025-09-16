import csv
import io
from datetime import date
def to_csv(rows, headers):
bio = io.StringIO()
writer = csv.writer(bio)
writer.writerow(headers)
for r in rows:
writer.writerow([r.get(h) for h in headers])
return bio.getvalue()