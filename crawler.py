#Initialize libraries
import sqlite3
import ssl
import lesscode_lib as lcode
#End Libraries

#ssl is anoying, ignore it
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode=ssl.CERT_NONE



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

#Cleaning input url
web_site = input('Type webpage to crawl\n')
site_page = lcode.clean_url(web_site, ctx) #Returns html/text

#find "likness"
pos = web_site.rfind('.')
clean = web_site[:pos]
pos = clean.rfind('www.')
if pos != -1: clean = clean[pos+4:]
pos = clean.rfind('//')
if pos != -1: clean = clean[pos+2:]


#Checking crawling status
cur.execute('''SELECT * FROM Websites WHERE url LIKE ?  ''', ('%'+clean+'%',))
row = cur.fetchone()
if row is None:
	cur.execute('''
	INSERT OR IGNORE INTO Websites (url) VALUES ( ? )
	''', (web_site,)   )
	cur.execute('''
	INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (?,NULL,1.0)
	''', (web_site,)    )
	conn.commit()
else:
	print ('Restarting existing crawl\n')

cur.execute('SELECT url FROM Websites')
webs = []
for row in cur:
	webs.append(str(row[0]))
print(webs)

cur.close()
