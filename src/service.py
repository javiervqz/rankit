from sqlite3 import connect
from os import lstat
from webParser import LinkParser, time_it
from datetime import datetime

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
    def crawling(self, web_site,state='C'):
           
        with connect(self.db_path) as sqlConn:
            cur = sqlConn.cursor()

            if state == 'S':
                main_crawl = LinkParser(web_site) 
                links, html, url = main_crawl.getLinks()

                cur.execute('''
                    INSERT OR IGNORE INTO Websites (url) VALUES (?)
                    '''
                    ,(url,))
                cur.execute('''
                    SELECT id from Websites WHERE url = ?
                    '''
                    ,(url,))
                id_website = cur.fetchone()[0]
                cur.execute('''
                    INSERT OR IGNORE INTO Pages (url,html,error,old_rank,new_rank, id_website)
                    VALUES (?,?,?,0,1,?)'''
                    ,(url,memoryview(html),100,id_website))

                for link in links:
                    cur.execute('''
                        INSERT OR IGNORE INTO Pages (url,error,old_rank,new_rank, id_website)
                        VALUES (?,120,0,1,?)'''
                        ,(link,id_website))

                    cur.execute('''
                        SELECT id FROM Pages WHERE url = ?'''
                        ,(link,))

                    to_id = cur.fetchone()[0]

                    cur.execute('''
                        INSERT OR IGNORE INTO Links (from_id, to_id)
                        VALUES (?,?)'''
                        ,(id_website,to_id))


            elif state == 'C':
                cur.execute('''
                    SELECT id, html, url FROM Pages WHERE error = 120
                    ORDER BY RANDOM() LIMIT 1''')
                random_pg = cur.fetchone()
                ##Likely root cause for bug in links when page is not main
                main_crawl = LinkParser(random_pg[2])
                print(random_pg[2])
                links, html, url = main_crawl.getLinks()
                from_id = random_pg[0]
                cur.execute('''
			UPDATE Pages SET error = 100, html = ? WHERE id = ? '''
                        , (memoryview(html),from_id,))

                print(links)
                for link in links:
                    cur.execute('''
                        INSERT OR IGNORE INTO Pages (url,error,old_rank,new_rank, id_website)
                        VALUES (?,120,0,1,?)'''
                        ,(link,1)) ##Remove Harcoded id_website

                    cur.execute('''
                        SELECT id FROM Pages WHERE url = ?'''
                        ,(link,))


                    to_id = cur.fetchone()[0]
                    print(f'to_id: {to_id}')
                    cur.execute('''
                        INSERT OR IGNORE INTO Links (from_id, to_id)
                        VALUES (?,?)'''
                        ,(from_id,to_id))



                print(f'url: {url} and from_id: {from_id}')
            else:
                raise Exception(f'Crawl state Unreachable {state}')



    def start_crawl(self, web_site):
        try:
           db_stat = lstat(self.db_path)
           datetime_obj = datetime.fromtimestamp(int(db_stat.st_ctime))
           print(f'Last modified :{datetime_obj}, size: {db_stat.st_size/1024} bytes')
           self.crawling(web_site)


        except FileNotFoundError:
            self._initializeDB()
            print(f'{self.db_path} initialized correctly')
            self.crawling(web_site,state='S')



