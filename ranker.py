import sqlite3



toRank = input('Type DB to Rank:\n')

conn = sqlite3.connect('DataBases/'+toRank)
cur = conn.cursor()

cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = []
for row in cur:
	from_ids.append(row[0])


to_ids = []
links = []
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for row in cur:
	from_id = row[0]
	to_id = row[1]
	if from_id == to_id: continue #zero diagonal
	if from_id not in from_ids: continue #Lone nodes
	if to_id not in from_ids: continue #Lone nodes
	links.append(row)
	if to_id not in to_ids:
		to_ids.append(to_id)


prev_ranks = {}
for node in from_ids:
	cur.execute('SELECT new_rank FROM Pages WHERE id = ?', (node,))
	row = cur.fetchone()
	prev_ranks[node] = row[0]

sval = input('How many iterations')
many = 1
if (len(sval) > 0): many = int(sval)
if (len(prev_ranks) < 1 ):
	print ('Nothing to rank, check data')
	quit()

for i in range(many):
	next_ranks = {}
	total = 0.0
	for (node, old_rank) in list(prev_ranks.items()):
		total += old_rank
		next_ranks[node] = 0.0


	for (node, old_rank) in list(prev_ranks.items()):
		give_ids = list()
		for (from_id, to_id) in links:
			if from_id != node: continue
			if to_id not in to_ids: continue
			give_ids.append(to_id)

		if (len(give_ids) < 1): continue
		amount = old_rank / len(give_ids)

		for idd in give_ids:
			next_ranks[idd] += amount

	newtot = 0
	for (node, next_rank) in list(next_ranks.items()):
		newtot += next_rank
	evap = (total - newtot)/ len(next_ranks)

	for node in next_ranks:
		next_ranks[node] += evap

	newtot = 0
	for(node, next_rank) in list(next_ranks.items()):
		newtot += next_rank

	totdiff = 0
	for (node, old_rank) in list(prev_ranks.items()):
		new_rank = next_ranks[node]
		diff = abs(old_rank - new_rank)
		totdiff += diff
	avediff = totdiff/len(prev_ranks)
	print (i + 1, avediff)

	prev_ranks = next_ranks

print(list(next_ranks.items())[:5])
cur.execute('UPDATE Pages SET old_rank=new_rank')
for (idd, new_rank) in list(next_ranks.items()):
	cur.execute('UPDATE Pages SET new_rank = ? WHERE id=?', (new_rank, idd))
conn.commit()
cur.close()
