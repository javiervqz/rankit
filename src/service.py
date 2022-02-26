from sqlite3 import connect
from os import lstat
from webParser import LinkParser, time_it

class CrawlService:
    def __init__(self,table_name,path='.'):
        self.table_name=table_name
        self.path = path
        self.db_path = '/'.join([self.path,self.table_name])

    def _initializeDB(self):
        try:
            lstat(self.path)
        except FileNotFoundError:
            print(f'Directoy not found for {self.db_path}, leave path blank or create directory')
            exit(69)

        with connect(self.db_path) as sqlConn:

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
    def crawling(self, web_site):
        main_crawl = LinkParser(web_site) 
        links, html, url = main_crawl.getLinks()
        with connect(self.db_path) as sqlConn:
           cur = sqlConn.cursor()

           cur.execute('''
                   INSERT OR IGNORE INTO Websites (url) VALUES (?)
                   ''',
                (url,)
                )
           cur.execute(''' SELECT id FROM Websites WHERE url = ?''',
                (url,))

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

##               cur.execute('''
##                    SELECT ID FROM Pages WHERE url = ? ''',
##                    (web_site,))
##               to_id = cur.fetchone()[0]


    def start_crawl(self, web_site):
        try:
           lstat(self.db_path)
           print('TODO')

        except FileNotFoundError:
            self._initializeDB()
            print(f'{self.db_path} initialized correctly')
            self.crawling(web_site)
















