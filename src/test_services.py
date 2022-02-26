from service import CrawlService


##init_db = CrawlService('name_db',path='asdfg')._initializeDB()
init_db_nopath = CrawlService('name_db').start_crawl('fing.uach.mx')


