import sqlite3

conn = sqlite3.connect('DataBases/Crawled_bu.BU')
cur = conn.cursor()

print("Crating JSON file\n")
nodesUse = int(input("How many node?\n"))

cur.execute('''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url)
               FROM Pages JOIN Links ON Pages.id = Links.to_ids
               WHERE html IS NOT NULL and ERROR = 100
               GROUP BY id ORDER BY id, inbound ''')

fhand = open('Crawled.js', 'w')
nodes = list()
maxRank = None
minRank = None
