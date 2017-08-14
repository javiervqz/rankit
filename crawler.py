#Initialize libraries
import sqlite3
from urllib.request import urlopen
from urllib.error import URLError
import sys
#End Libraries


conn = sqlite3.connect('Crawled.DB')
cur = conn.cursor()
#Create schema for DB
cur.executescript('''
CREATE TABLE IF NOT EXISTS Pages(
id INTEGER PRIMARY KEY,
url TEXT UNIQUE,
html TEXT,
error INTEGER,
old_rank REAL,
new_rank REAL
id_website INTEGER
);

CREATE TABLE IF NOT EXISTS Websites(
id INTEGER PRIMARY KEY,
url TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Links(
from_id INTEGER,
to_id INTEGER
)
''')


web_site = input('Type webpage to crawl\n')
if (web_site.endswith('/') ) : web_site = web_site[:-1]
if ( web_site.endswith('.htm') or web_site.endswith('.html') ) :
	pos = web_site.rfind('/')
	web_site = web_site[:pos]
if not web_site.startswith('http://') or web_site.startswith('https://'):
	try:
		web_site = 'http://'+web_site
		doc = urlopen(web_site)
	except:
		try:
			web_site = 'http://www.'+web_site[7:]
			doc = urlopen(web_site)
		except URLError as doc:
			print ('Not Found\t',doc)
			sys.exit(0)


cur.execute('SELECT * FROM Websites WHERE url = ?', (web_site,))
row = cur.fetchone()
if row is None:
	cur.execute('''
	INSERT INTO Websites (url) VALUES ( ? )
	''',(web_site,))

else:
	cur.execute('''
	SELECT id,url FROM Pages WHERE html IS NULL and error is NULL
	ORDER BY RANDOM() LIMIT 1''')
	row = cur.fetchone()
	if row is not None:
		print ('Restarting existing crawl')
	else:
		cur.execute('''
		INSERT INTO Pages (url, html, new_rank) VALUES (?,NULL,1.0)''',
		(web_site,))


conn.commit()
cur.close()
