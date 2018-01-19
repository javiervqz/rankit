#Initialize libraries
import sqlite3
from classes import LinkParser
#End Libraries

#ssl is anoying, ignore it


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
	cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank, id_website) VALUES (?, ?, 1.0, ?) ''', (BaseUrl,memoryview(html), id_website))
else:
	id_website = row[0]
	print('Restarting existing crawl \n')

# while True:
links = BaseWeb.GetLinks(html)
for link in links:
	print ('Working')
	WebBranch = LinkParser()
	html, BranchUrl = WebBranch.CleanUrl(link)
	cur.execute('''SELECT id FROM Pages WHERE url = ?''', (BaseUrl,))
	from_id = cur.fetchone()[0]
	if len(html) != -1  and BranchUrl != 'None html page':
		cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank, id_website) VALUES (?, NULL, 0.-1, ?) ''', (BranchUrl , id_website))
		cur.execute('''SELECT id FROM Pages WHERE url = ?''', (BranchUrl,))
		to_id = cur.fetchone()[0]
		cur.execute('''INSERT OR IGNORE INTO Links (from_id, to_id) VALUES  (?, ?)''', (from_id, to_id))
print ('done')

conn.commit()
cur.close()
