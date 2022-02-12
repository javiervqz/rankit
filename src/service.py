from sqlite3 import connect
from webParser import LinkParser, time_it

class CrawlService:
    def __init__(self,table_name):
        self.table_name=table_name

    def _initializeDB(self, path=''):
        #table_path = ''.join([path,self.table_name])
        with connect(self.table_name) as sqlConn:
            cur = sqlConn.cursor()
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
            '''
            )
    @time_it
    def start_crawl(self, web_site):
       main_crawl = LinkParser(web_site) 
       links, html, url = main_crawl.getLinks()
       self._initializeDB()
       with connect(self.table_name) as sqlConn:
           cur = sqlConn.cursor()
           cur.execute('''
                   INSERT OR IGNORE INTO Websites (url) VALUES (?)
                   ''',
                (url,)
                )
           cur.execute(''' SELECT id FROM Websites''')
           id_website = cur.fetchone()[0]
           cur.execute('''
                INSERT OR IGNORE INTO Pages 
                (url, html, new_rank, id_website, error)
                VALUES (?,?,1.0,?,100)
                ''',
                (url,memoryview(html),id_website)
                )
           for link in links:
               cur.execute('''
                    INSERT OR IGNORE INTO Pages
                    (url, new_rank, id_website,error)
                    VALUES (?,1.0, ?, 120)
                    ''',
                    (link,id_website)
                    )
















