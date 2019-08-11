import sqlite3

conn = sqlite3.connect('Crawled.db')
cur = conn.cursor()

cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = []
for row in cur:
	from_ids.append(row[0])

to_ids = []
links = []
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for row in cur:
	from_id = row[0]
	to_id = row[1]
	if from_id == to_id: continue
	if from_id not in from_ids: continue
	if to_id not in from_ids: continue
	links.append(row)
	if to_id not in to_ids:
		to_ids.append(to_id)

print(len(from_ids), len(to_ids))
print(len(links))
for ids in from_ids:
	if ids not in to_ids:
		print(ids)
