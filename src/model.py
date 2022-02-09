class parsedWebsite:
    def __init__(self,url):
        self.url = url

    @staticmethod
    def schema():
        return '''
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
        )'''
