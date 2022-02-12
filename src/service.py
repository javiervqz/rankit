from sqlite3 import connect

class crawlService:
    def __init__(self,table_name):
        self.table_name=table_name

    def _initializeDB(self):
        sqlConn = connect(self.table_name) 
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

        CREATE TABLE IF NOT EXISTS Links(
        from_id INTEGER,
        to_id INTEGER
        )
        '''
        )

        sqlConn.commit()
        cur.close()

