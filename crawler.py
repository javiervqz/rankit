#Initialize libraries
import sqlite3
import ssl
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
new_rank REAL,
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

#Cleaning input url outputs html and url
web_site = input('Type webpage to crawl\n')
site_page, web_site = lcode.clean_url(web_site, ctx)

#This will only left the name of the website, without the host or protocols
pos = web_site.rfind('.')#gets first point from string's end
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
	INSERT OR IGNORE INTO Websites (url) VALUES ( ? )''',
	(web_site,)   )
	cur.execute('''
	SELECT id FROM Websites''')
	id_website = cur.fetchone()[0]
	cur.execute('''
	INSERT OR IGNORE INTO Pages (url, html, new_rank, id_website)
	VALUES (?,NULL,1.0, ?)
	''', (web_site,id_website)    )
	conn.commit()
else:
	id_website = row[0]
	print ('Restarting existing crawl\n')


#Showing wesites
cur.execute('SELECT url,id FROM Websites')
webs = []
for row in cur:
	webs.append(str(row[0]))
print(webs)


many = 0
while True:
	if (many == 0):
		scal = input('How many pages: ')
		if (len(scal) < 1): break
		many = int(scal)
	print ('\n\t\t',many,'\t\t\n')
	many-=1
#Verifying if url was gathered already



	cur.execute('''SELECT id,url FROM Pages WHERE html IS NULL
	AND error is NULL AND url LIKE ?
	ORDER BY RANDOM() LIMIT 1 ''', ('%'+clean+'%',))

	try:
		row = cur.fetchone()
		fromid = row[0]
		url = row[1]
	except:
		print('\033[1m'+'No unretrieve HTML pages found'+'\033[0m')
		many = 0
		break
	print(fromid, url, end=' ')
#Checking for errors on site, or during process (network, interruption)
	try:
		cur.execute('DELETE FROM Links WHERE from_id = ?',(fromid,))
		#first_check = True
		html = site_page.read()
		html = html.strip()
		if (len(html) == 0):
			first_check = False
			site_page, url = lcode.clean_url(url,ctx)
			html = site_page.read()
			html = html.strip()
		if site_page.getcode() != 200:
			print('Error on page', site_page.getcode())
			cur.execute('UPDATE Pages SET error=? WHERE url=?',
					(site_page.getcode(), url))
			many += 1
		if 'text/html' != site_page.info().get_content_type():
			#if not first_check:
			ignore = url[-4:]

			print('\033[1m'+'Ignore non text/html page'+'\033[0m')
			cur.execute('DELETE FROM Pages WHERE url LIKE ?',('%'+ignore,))
			many += 1
			continue


		soup = BeautifulSoup(html, 'html.parser')
		print('Characters ('+str(len(html))+')', end =' ')
	except KeyboardInterrupt:
		print('\033[1m'+'Interrupted'+'\033[0m')
		break
	except:
		print('\033[1m'+'Unable to retrieve or parse'+'\033[0m')
		cur.execute('UPDATE Pages SET error=-1 WHERE url=?',(url, ))
		many += 1
		conn.commit()
		continue

#Done checking for errors, lets get the info


	cur.execute('''
	INSERT OR IGNORE INTO Pages(url, html, new_rank, id_website)
	VALUES(?, NULL, 1.0, ?) ''',
	(url,id_website))
	cur.execute('''UPDATE Pages SET html=? WHERE url=?''',
				(memoryview(html),url))
#Retrieving new urls
	tags = soup('a')
	i = 0
	for tag in tags:
		href = tag.get('href', None)
		if (href is None): continue
	#Solve weird references like href'/facultad/2017'
		href = href.strip()
		up = urlparse(href)
		if (len(up.scheme)<1):
			href=urljoin(url,href)
		ipos = href.find('#')
		if(ipos>1):href = href[:ipos]
		if (href.endswith('/')): href = href[:-1]
		#print (href)

		found = False
		for web in webs:
			if (href.startswith(web)):
				found = True
				break
		if not found: continue




		cur.execute('''
		INSERT OR IGNORE INTO Pages (url,html,new_rank) VALUES (?,NULL,1.0)''',
		(href, ))
		conn.commit()

		cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', (href,))
		try:
			row = cur.fetchone()
			toid=row[0]
		except:
			print('\033[1m'+'Could not retrieve ID'+'\033[0m')
			continue
		cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES (?,?)',
					(fromid, toid))

conn.commit()
cur.close()
