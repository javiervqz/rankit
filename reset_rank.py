import sqlite3
from numpy import around
conn = sqlite3.connect('Crawled.db')
cur = conn.cursor()

cur.execute('SELECT id FROM Pages')
no_pages = len(cur.fetchall())
start = 100.0/no_pages

# cur.execute('UPDATE Pages SET new_rank = ? ', (1.0,))

cur.execute('SELECT SUM(new_rank) FROM Pages')
result = around([cur.fetchone()[0]], decimals=1)
if result[0] != 100.0:
	print ('''There is data lost or reset did not run correctly\n
			Pagerank total {}'''.format(result[0]))
conn.commit()
cur.close()

print ("{} pages set to rank {}".format(no_pages, start))
