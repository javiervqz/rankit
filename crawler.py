#Initialize libraries
import sqlite3
import ssl
import sys
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
import functions as lcode
from bs4 import BeautifulSoup
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
to_id INTEGER UNIQUE
)
''')

#Cleaning input url
web_site = input('Type webpage to crawl\n')
site_page, web_site = lcode.clean_url(web_site, ctx) #Returns HTTPResponse object


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


many = 0
while True:
	if (many < 1):
		scal = input('How many pages: ')
		if (len(scal) < 1): break
		many = int(scal)
	many -= 1
#Verifying if url was gathered already
	cur.execute('''SELECT id,url FROM Pages WHERE html IS NULL AND error is NULL
	ORDER BY RANDOM() LIMIT 1 ''')
	try:
		row = cur.fetchone()
		fromid = row[0]
		url = row[1]
	except:
		print('No unretrieve HTML pages found')
		many = 0
		break
	print(fromid, url, end=' ')
#Checking for errors on site, or during process (network, interruption)
	try:
		cur.execute('DELETE FROM Links WHERE from_id = ?',(fromid,))
		html = site_page.read()
		if site_page.getcode() != 200:
			print('Error on page', site_page.getcode())
			cur.execute('UPDATE Pages SET error=? WHERE url=?',
					(site_page.getcode(), url))
		if 'text/html' != site_page.info().get_content_type():
			print('Ignore non text/html page')
			cur.execute('DELETE FROM Pages WHERE url=?',(url,))
			continue
		soup = BeautifulSoup(html, 'html.parser')
		print('Characters ('+str(len(html))+')', end =' ')
	except KeyboardInterrupt:
		print('Interrupted')
		break
	except:
		print('Unable to retrieve or parse')
		cur.execute('UPDATE Pages SET error=-1 WHERE url=?',(url, ))
		conn.commit()
		continue

#Done checking for errors, lets get the info

	cur.execute('''
	INSERT OR IGNORE INTO Pages(url, html, new_rank) VALUES(?, NULL, 1.0) ''',
	(url,))
	cur.execute('UPDATE Pages SET html=? WHERE url=?',(memoryview(html),url))
	conn.commit()
#Retrieving new urls
	tags = soup('a')
	count = 0
	for tag in tags:
		href = tag.get('href', None)
		if (href is None): continue
	#Solve weird references like href'/facultad/2017'
		up = urlparse(href)
		if (len(up.scheme)<1):
			href=urljoin(url,href)
		ipos = href.find('#')
		if(ipos>1):href = href[:pos]
		if (href.endswith('/')): href = href[:-1]
		print (href)




		cur.execute('''
		INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (?,NULL,1.0)''',
		(href, ))
		count += 1
		conn.commit()

		cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', (href,))
		try:
			row = cur.fetchone()
			toid=row[0]
		except:
			print('Could not retrieve ID')
			continue
		cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES (?,?)',
					(fromid, toid))
	print(count)

cur.close()
