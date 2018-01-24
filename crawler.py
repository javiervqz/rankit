#Initialize libraries
import sqlite3
from classes import LinkParser
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
new_rank REAL,
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

#Cleaning input url outputs html and url
web_site = input('Type website to crawl\n')
BaseWeb = LinkParser()
html, BaseUrl = BaseWeb.CleanUrl(web_site)

cur.execute(''' SELECT * FROM Websites WHERE url LIKE ? ''', ('%'+web_site+'%',))
row = cur.fetchone()

if row is None:
	cur.execute('''INSERT OR IGNORE INTO Websites (url) VALUES (?)''', (BaseUrl,))
	cur.execute('''SELECT id FROM Websites''')
	id_website = cur.fetchone()[0]
	cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank, id_website, error) VALUES (?, ?, 1.0, ?, 120) ''', (BaseUrl,memoryview(html), id_website))
else:#You can add the continuation of the crawling here
	id_website = row[0]
	print('Restarting existing crawl \n')

i = 0
while i < 30:
	links = []
	print('Getting links from page {}'.format(i))
	cur.execute('''SELECT html, url FROM Pages WHERE error = 120 ORDER BY RANDOM() LIMIT 1''')
	row = cur.fetchone()
	html = row[0]
	BaseUrl = row[1]
	print ('{}, {}'.format(len(html), BaseUrl))
	cur.execute('''UPDATE Pages SET error = 100 WHERE url = ? ''', (BaseUrl,))
	links = BaseWeb.GetLinks(html)
	cur.execute('''SELECT id FROM Pages WHERE url = ? ''', (BaseUrl,))
	from_id = cur.fetchone()[0]
	print (links)
	for link in links:
		html, BaseUrl = BaseWeb.CleanUrl(link)
		if BaseUrl == "None html page":
			print ("Ignored page (not html)")
			continue
		elif html is None:
			cur.execute('''INSERT OR IGNORE INTO Pages (url, error) VALUES (?, 150)''', (BaseUrl,))
			conn.commit()
		else:
			print ("Getting new page")
			cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank, id_website, error) VALUES (?, ?, 1.0, ?, 120) ''', (BaseUrl, html, id_website))
			conn.commit()

		cur.execute('''SELECT id FROM Pages WHERE url = ? ''', (BaseUrl,))
		to_id = cur.fetchone()[0]
		if from_id != to_id:
			cur.execute('''INSERT OR IGNORE INTO Links (from_id, to_id) VALUES (?, ?)''', (from_id, to_id))
			conn.commit()

	i += 1



conn.commit()
cur.close()
